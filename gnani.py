"""Gnani speech APIs (Prisma and Timbre), with a credit guard and a free mock mode.

Mock mode is ON unless MOCK_GNANI=0 is set, so nothing spends credits by accident.
Paid calls are never retried automatically.
"""
import hashlib
import io
import json
import math
import os
import wave
from pathlib import Path

import httpx

BASE = "https://api.vachana.ai"
DATA = Path(os.getenv("MERI_DATA", Path(__file__).parent / "data"))
USAGE_FILE = DATA / "usage.json"

MOCK_LINES = {
    "pa-IN": ["ਤੁਸੀਂ ਰੋਟੀ ਖਾ ਲਈ?", "ਅੱਜ ਤਬੀਅਤ ਕਿਵੇਂ ਹੈ?", "ਮੈਂ ਤੁਹਾਨੂੰ ਮਿਲਣ ਆਵਾਂ?"],
    "hi-IN": ["आपने खाना खा लिया?", "आज तबीयत कैसी है?", "क्या मैं आपसे मिलने आऊँ?"],
}


class CreditGuardError(Exception):
    pass


class GnaniError(Exception):
    pass


def is_mock() -> bool:
    return os.getenv("MOCK_GNANI", "1") != "0"


def max_live_calls() -> int:
    return int(os.getenv("MAX_LIVE_GNANI_CALLS", "150"))


def usage() -> dict:
    if USAGE_FILE.exists():
        return json.loads(USAGE_FILE.read_text())
    return {"live_calls": 0, "mock_calls": 0}


def _count(mock: bool) -> None:
    current = usage()
    if not mock and current["live_calls"] >= max_live_calls():
        raise CreditGuardError(
            f"Stopped at {max_live_calls()} live Gnani calls to protect your credits. "
            "Raise MAX_LIVE_GNANI_CALLS in .env if you want more."
        )
    current["mock_calls" if mock else "live_calls"] += 1
    DATA.mkdir(parents=True, exist_ok=True)
    USAGE_FILE.write_text(json.dumps(current))


def _headers() -> dict:
    key = os.getenv("GNANI_API_KEY", "")
    if not key:
        raise GnaniError("GNANI_API_KEY is missing from .env")
    return {"X-API-Key-ID": key}


def _raise_for(resp: httpx.Response, what: str) -> None:
    if resp.status_code >= 400:
        raise GnaniError(f"{what} failed with HTTP {resp.status_code}: {resp.text[:300]}")


def _mock_wav(text: str) -> bytes:
    """A soft tone whose length follows the text. Clearly not a real voice."""
    rate = 16000
    seconds = min(4.0, 0.4 + len(text) * 0.04)
    frames = bytearray()
    for i in range(int(rate * seconds)):
        fade = min(1.0, i / 800, (rate * seconds - i) / 800)
        value = int(5000 * fade * math.sin(2 * math.pi * 330 * i / rate))
        frames += value.to_bytes(2, "little", signed=True)
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(frames))
    return out.getvalue()


def transcribe(wav: bytes, language: str, keyterms=None, previous_text: str = "") -> dict:
    """Transcribe up to 30 s of WAV audio with Prisma v3.0."""
    if is_mock():
        _count(True)
        lines = MOCK_LINES.get(language, MOCK_LINES["pa-IN"])
        index = int(hashlib.sha1(wav).hexdigest(), 16) % len(lines)
        return {"transcript": lines[index], "detected_language_code": language, "mock": True}

    _count(False)
    # Only the chosen language plus English: Hindi and Punjabi sound alike, and allowing both
    # made Prisma sometimes write a Hindi answer in Punjabi letters.
    data = {"model": "prisma-v3.0", "language_code": f"{language},en-IN"}
    if keyterms:
        data["keyterms"] = json.dumps(list(keyterms)[:200], ensure_ascii=False)
    if previous_text.strip():
        data["previous_text"] = previous_text[-600:]
    resp = httpx.post(
        f"{BASE}/stt/v3",
        headers=_headers(),
        files={"audio_file": ("audio.wav", wav, "audio/wav")},
        data=data,
        timeout=60,
    )
    _raise_for(resp, "Speech to text")
    body = resp.json()
    return {
        "transcript": body.get("transcript", ""),
        "detected_language_code": body.get("detected_language_code"),
        "mock": False,
    }


def create_voice(wav: bytes) -> dict:
    """Turn one clean 5-30 s clip into a reusable speaker embedding."""
    if is_mock():
        _count(True)
        return {"embedding": "mock", "shape": [1, 768], "dtype": "torch.bfloat16"}

    _count(False)
    resp = httpx.post(
        f"{BASE}/api/v1/tts/voice-clone/embeddings",
        headers=_headers(),
        files={"audio_file": ("voice.wav", wav, "audio/wav")},
        timeout=120,
    )
    _raise_for(resp, "Voice cloning")
    body = resp.json()
    embedding = (body.get("data") or {}).get("voice_clone_embedding") or body.get("voice_clone_embedding") or body
    if not all(k in embedding for k in ("embedding", "shape", "dtype")):
        raise GnaniError(f"Unexpected voice cloning response: {str(body)[:300]}")
    return {k: embedding[k] for k in ("embedding", "shape", "dtype")}


AUDIO_CONFIG = {
    "sample_rate": 24000,
    "num_channels": 1,
    "sample_width": 2,
    "encoding": "linear_pcm",
    "container": "wav",
}


def speak_cloned(text: str, voice: dict) -> bytes:
    if is_mock():
        _count(True)
        return _mock_wav(text)

    _count(False)
    resp = httpx.post(
        f"{BASE}/api/v1/tts/inference",
        headers={**_headers(), "Content-Type": "application/json"},
        json={
            "text": text,
            "model": "vachana-vc-v1",
            "speaker_embedding": voice,
            "audio_config": AUDIO_CONFIG,
        },
        timeout=120,
    )
    _raise_for(resp, "Cloned speech")
    return resp.content


def speed() -> float:
    """Timbre speaking speed, 0.85 to 1.15. A little slower than normal sounds calmer for small children."""
    try:
        return round(min(1.15, max(0.85, float(os.getenv("TTS_SPEED", "0.85")))), 2)
    except ValueError:
        return 0.85


def speak_timbre(text: str, language: str, voice: str = "") -> bytes:
    """Speak with one of Timbre v3.0's built-in voices."""
    if is_mock():
        _count(True)
        return _mock_wav(text)

    _count(False)
    resp = httpx.post(
        f"{BASE}/api/v1/tts/inference",
        headers={**_headers(), "Content-Type": "application/json"},
        json={
            "text": text,
            "model": "timbre-v3.0",
            "voice": voice or os.getenv("BEBE_VOICE", "Lakshmi"),
            "language": language,
            "speed": speed(),
            "audio_config": AUDIO_CONFIG,
        },
        timeout=120,
    )
    _raise_for(resp, "Speech")
    return resp.content
