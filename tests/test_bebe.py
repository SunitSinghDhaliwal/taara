"""Mock mode only: no Gnani credits are spent."""
import array
import io
import math
import os
import sys
import tempfile
from pathlib import Path

os.environ["MOCK_GNANI"] = "1"
os.environ["MERI_DATA"] = tempfile.mkdtemp()
os.environ["LLM_API_KEY"] = ""
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

import audio_utils  # noqa: E402
import gnani  # noqa: E402
import server  # noqa: E402
from grade import grade  # noqa: E402
from lessons import CONTENT, all_keys, line_text  # noqa: E402

client = TestClient(server.app)
PA = CONTENT["pa-IN"]


def wav(seconds, loud=True):
    samples = array.array("h", (int((6000 if loud else 0) * math.sin(i / 8)) for i in range(int(16000 * seconds))))
    return audio_utils.to_wav(16000, samples.tobytes())


def lesson(i=2):
    return PA["lessons"][i]


def test_every_line_resolves():
    for lang in CONTENT:
        for key in all_keys(lang):
            assert line_text(lang, key)


def test_unknown_line_rejected():
    assert client.post("/api/line", json={"lang": "pa-IN", "key": "free:anything"}).status_code == 404


def test_exact_answer_passes_without_llm():
    assert grade("ਹਾਂ ਜੀ ਮੈਂ ਰੋਟੀ ਖਾ ਲਈ", lesson(), "Punjabi")["by"] == "match"


def test_roman_answer_passes():
    assert grade("haan ji main roti kha lai", lesson(), "Punjabi")["label"] == "said_it"


def test_partial_answer_counts_as_tried_offline():
    assert grade("ਰੋਟੀ", lesson(), "Punjabi")["label"] in {"tried", "said_it"}


def test_english_detected_offline():
    assert grade("yes I ate pizza", lesson(), "Punjabi")["label"] == "english"


def test_prepare_caches_everything():
    first = client.post("/api/prepare", json={"lang": "pa-IN"}).json()
    calls = gnani.usage()["mock_calls"]
    second = client.post("/api/prepare", json={"lang": "pa-IN"}).json()
    assert first["made"] == first["total"] and second["made"] == 0
    assert gnani.usage()["mock_calls"] == calls


def test_answer_and_progress():
    files = {"audio": ("a.wav", io.BytesIO(wav(2)), "audio/wav")}
    body = client.post("/api/answer", files=files, data={"lang": "pa-IN", "lesson_id": "roti"}).json()
    assert body["heard"] and body["label"] in {"said_it", "tried", "english", "other"}
    assert client.get("/api/content").json()["progress"]["log"]


def test_silence_costs_nothing():
    calls = gnani.usage()["mock_calls"]
    files = {"audio": ("a.wav", io.BytesIO(wav(2, False)), "audio/wav")}
    assert client.post("/api/answer", files=files, data={"lang": "pa-IN", "lesson_id": "roti"}).json()["label"] == "silent"
    assert gnani.usage()["mock_calls"] == calls


def test_family_phrase_added_and_spoken():
    item = client.post("/api/custom", json={"lang": "hi-IN", "ask": "चाचू कैसे हैं?", "target": "चाचू ठीक हैं", "target_en": "Chachu is fine"}).json()
    ids = [x["id"] for x in client.get("/api/content").json()["content"]["hi-IN"]["lessons"]]
    assert item["id"] in ids
    assert client.post("/api/line", json={"lang": "hi-IN", "key": f"ask:{item['id']}"}).status_code == 200
    assert client.post("/api/line", json={"lang": "hi-IN", "key": f"slow:{item['id']}"}).status_code == 200
    client.delete(f"/api/custom/hi-IN/{item['id']}")


def test_word_tracks_and_fix_lines():
    hi = client.get("/api/content").json()["content"]["hi-IN"]
    assert len(hi["tracks"]) == 9
    item = hi["tracks"][1]["items"][0]
    assert client.post("/api/line", json={"lang": "hi-IN", "key": f"ask:{item['id']}"}).status_code == 200
    assert client.post("/api/line", json={"lang": "hi-IN", "key": "word:roti:2"}).status_code == 200
    assert line_text("hi-IN", "word:roti:2") == "<slow> मैंने"
    files = {"audio": ("a.wav", io.BytesIO(wav(2)), "audio/wav")}
    assert client.post("/api/answer", files=files, data={"lang": "hi-IN", "lesson_id": item["id"]}).status_code == 200


def test_translate_guardrails_without_key():
    r = client.post("/api/translate", json={"lang": "hi-IN", "text": "my number is 9876543210"})
    assert r.status_code == 422
    r = client.post("/api/translate", json={"lang": "hi-IN", "text": "I ate pizza"})
    assert r.status_code == 422  # no Groq key in tests


def test_translation_spoken_only_if_stored():
    assert client.post("/api/line", json={"lang": "hi-IN", "key": "tr:doesnotexist"}).status_code == 404


def test_relative_changes_lines_and_grammar():
    client.post("/api/profile", json={"lang": "hi-IN", "relative": "dada", "name": "Aarav", "gender": "boy"})
    hi = client.get("/api/content").json()["content"]["hi-IN"]
    assert hi["lessons"][0]["target"] == "नमस्ते दादा जी"
    assert "होंगे" in hi["praise"][0]
    assert client.post("/api/line", json={"lang": "hi-IN", "key": "greet"}).status_code == 200
    assert client.post("/api/line", json={"lang": "hi-IN", "key": "en:roti"}).status_code == 200
    assert client.post("/api/line", json={"lang": "hi-IN", "key": "find:w-colours-0"}).status_code == 200
    assert client.post("/api/profile", json={"name": "<script>"}).status_code == 400
    client.post("/api/profile", json={"lang": "hi-IN", "relative": "dadi"})
