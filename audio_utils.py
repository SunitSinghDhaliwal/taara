"""WAV helpers. The browser always sends 16 kHz mono 16-bit WAV."""
import array
import io
import wave

MAX_CHUNK_SECONDS = 28
MIN_CHUNK_SECONDS = 18


class AudioError(Exception):
    pass


def read_wav(data: bytes):
    try:
        with wave.open(io.BytesIO(data), "rb") as w:
            if w.getsampwidth() != 2 or w.getnchannels() != 1:
                raise AudioError("Audio must be 16-bit mono WAV")
            return w.getframerate(), w.readframes(w.getnframes())
    except (wave.Error, EOFError) as exc:
        raise AudioError("That audio could not be read as WAV") from exc


def to_wav(rate: int, frames: bytes) -> bytes:
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(frames)
    return out.getvalue()


def duration(data: bytes) -> float:
    rate, frames = read_wav(data)
    return len(frames) / 2 / rate


def is_silent(data: bytes, threshold: int = 250) -> bool:
    _, frames = read_wav(data)
    samples = array.array("h", frames)
    if not samples:
        return True
    return sum(abs(s) for s in samples) / len(samples) < threshold


def _quietest_cut(samples, rate: int, start: int, end: int) -> int:
    """Index of the quietest 100 ms window in samples[start:end]."""
    window = rate // 10
    best, best_energy = end, None
    for pos in range(start, max(start + 1, end - window), window):
        energy = sum(abs(s) for s in samples[pos : pos + window])
        if best_energy is None or energy < best_energy:
            best, best_energy = pos + window // 2, energy
    return best


def split_for_rest(data: bytes) -> list:
    """Split long audio at quiet moments into clips under the 30 s REST limit."""
    rate, frames = read_wav(data)
    samples = array.array("h", frames)
    chunks, pos = [], 0
    while len(samples) - pos > MAX_CHUNK_SECONDS * rate:
        cut = _quietest_cut(samples, rate, pos + MIN_CHUNK_SECONDS * rate, pos + MAX_CHUNK_SECONDS * rate)
        chunks.append(to_wav(rate, samples[pos:cut].tobytes()))
        pos = cut
    if len(samples) - pos > rate // 2:
        chunks.append(to_wav(rate, samples[pos:].tobytes()))
    return chunks
