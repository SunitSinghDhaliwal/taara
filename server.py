"""Taara, aapki India se dost: kids abroad learn to talk with their grandparents and relatives."""
import hashlib
import json
import re
import unicodedata
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile  # noqa: E402
from fastapi.responses import FileResponse, JSONResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel  # noqa: E402

import audio_utils  # noqa: E402
import gnani  # noqa: E402
from grade import grade  # noqa: E402
import translate as tr  # noqa: E402
import chat  # noqa: E402
from lessons import CONTENT, GREET_FRAME, RELATIVES, all_keys, line_text, localize, tracks, word_items  # noqa: E402

DATA = gnani.DATA
AUDIO = DATA / "audio"
PROGRESS = DATA / "progress.json"
CUSTOM = DATA / "custom.json"
TRANSLATIONS = DATA / "translations.json"
RANK = {"tried": 1, "said_it": 2}

app = FastAPI(title="Taara")


@app.exception_handler(gnani.CreditGuardError)
async def on_guard(_: Request, exc: Exception):
    return JSONResponse({"detail": str(exc)}, status_code=429)


@app.exception_handler(gnani.GnaniError)
async def on_gnani(_: Request, exc: Exception):
    return JSONResponse({"detail": str(exc)}, status_code=502)


@app.exception_handler(tr.TranslateError)
async def on_translate(_: Request, exc: Exception):
    return JSONResponse({"detail": str(exc)}, status_code=422)


@app.exception_handler(audio_utils.AudioError)
async def on_audio(_: Request, exc: Exception):
    return JSONResponse({"detail": str(exc)}, status_code=400)


def load_progress() -> dict:
    progress = json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {}
    progress.setdefault("lessons", {})
    progress.setdefault("log", [])
    progress.setdefault("calls_done", {})
    progress.setdefault("game", {"xp": 0, "best_streak": 0, "stars": {}, "badges": [], "today": {"date": "", "count": 0}})
    progress.setdefault("profile", {"name": "", "gender": "", "relative": {}})
    return progress


def rel_of(lang: str):
    return load_progress()["profile"]["relative"].get(lang)


def child_name() -> str:
    return load_progress()["profile"]["name"]


class Profile(BaseModel):
    lang: str = ""
    relative: str = ""
    name: str | None = None
    gender: str | None = None


@app.post("/api/profile")
def set_profile(body: Profile):
    progress = load_progress()
    profile = progress["profile"]
    if body.lang and body.relative:
        if body.lang not in RELATIVES or body.relative not in {r["id"] for r in RELATIVES[body.lang]}:
            raise HTTPException(400, "Unknown relative")
        profile["relative"][body.lang] = body.relative
    if body.name is not None:
        name = " ".join(body.name.split())[:20]
        if name and not all(c.isalpha() or c in " '-" or unicodedata.category(c).startswith("M") for c in name):
            raise HTTPException(400, "Please use letters only for the name")
        profile["name"] = name
    if body.gender is not None:
        profile["gender"] = body.gender if body.gender in {"boy", "girl"} else ""
    save_progress(progress)
    return progress


def save_progress(progress: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    PROGRESS.write_text(json.dumps(progress, ensure_ascii=False, indent=1))


def load_custom() -> dict:
    return json.loads(CUSTOM.read_text()) if CUSTOM.exists() else {}


def lessons_of(lang: str) -> list:
    return localize(lang, rel_of(lang))["lessons"] + load_custom().get(lang, [])


def load_translations() -> dict:
    return json.loads(TRANSLATIONS.read_text()) if TRANSLATIONS.exists() else {}


def translate_cached(english: str, lang: str) -> dict:
    store = load_translations()
    item = store.get(tr.tr_id(lang, english, load_progress()["profile"]["gender"]))
    if item:
        return item
    item = tr.translate(english, lang, load_progress()["profile"]["gender"])
    store[item["id"]] = item
    DATA.mkdir(parents=True, exist_ok=True)
    TRANSLATIONS.write_text(json.dumps(store, ensure_ascii=False, indent=1))
    return item


class Translate(BaseModel):
    lang: str
    text: str


@app.post("/api/translate")
def translate_text(body: Translate):
    check_lang(body.lang)
    return translate_cached(body.text, body.lang)


def remember(item: dict) -> dict:
    """Store an AI-written line so it can be spoken once, by id, and never regenerated."""
    item["id"] = hashlib.sha1(f"{item['lang']}|{item['native']}".encode()).hexdigest()[:12]
    store = load_translations()
    store[item["id"]] = item
    DATA.mkdir(parents=True, exist_ok=True)
    TRANSLATIONS.write_text(json.dumps(store, ensure_ascii=False, indent=1))
    return item


@app.post("/api/chat")
async def free_talk(lang: str = Form(...), history: str = Form("[]"), text: str = Form(""), audio: UploadFile | None = File(None)):
    """One turn of free talk: hear the child, then the pretend relative replies."""
    check_lang(lang)
    said = " ".join(text.split())[:200]
    if not said and audio is not None:
        wav = await audio.read()
        if len(wav) > 5 * 1024 * 1024 or audio_utils.duration(wav) > 25:
            raise HTTPException(400, "Please keep it short")
        if audio_utils.is_silent(wav, threshold=150):
            return {"heard": "", "reply": None}
        said = gnani.transcribe(wav, lang)["transcript"].strip()
    if not said:
        return {"heard": "", "reply": None}
    if re.search(r"\d{5,}|@|https?://", said):
        said = "(the child shared a number or link)"
    try:
        turns = json.loads(history)
        turns = turns if isinstance(turns, list) else []
    except ValueError:
        turns = []
    rel = localize(lang, rel_of(lang))["relative"]
    out = chat.reply(lang, rel, turns, said, load_progress()["profile"]["gender"])
    reply_item = remember({"lang": lang, "native": out["native"], "roman": out["roman"], "english": out["english"]})
    hint = None
    letters = [c for c in said if c.isalpha()]
    if letters and sum(c.isascii() for c in letters) / len(letters) > 0.6:
        # Typed or heard in English letters: give the family-language version reliably.
        try:
            t = translate_cached(said, lang)
            hint = {"id": t["id"], "native": t["native"], "roman": t["roman"]}
        except tr.TranslateError:
            hint = None
    elif out["hint"]:
        hint = remember({"lang": lang, "native": out["hint"]["native"], "roman": out["hint"]["roman"], "english": said})
    progress = load_progress()
    progress["log"] = (progress["log"] + [{"at": datetime.now(timezone.utc).isoformat(), "lang": lang, "lesson": "free-talk",
                                            "mode": "chat", "heard": said, "label": "chat"}])[-200:]
    save_progress(progress)
    return {"heard": said, "reply": reply_item, "hint": hint}


@app.post("/api/translate-audio")
async def translate_audio(audio: UploadFile = File(...), lang: str = Form(...)):
    check_lang(lang)
    wav = await audio.read()
    if len(wav) > 5 * 1024 * 1024 or audio_utils.duration(wav) > 20:
        raise HTTPException(400, "Please keep it short")
    if audio_utils.is_silent(wav, threshold=150):
        raise HTTPException(400, "I didn't hear anything. Try again.")
    heard = gnani.transcribe(wav, lang)["transcript"].strip()
    if not heard:
        raise HTTPException(400, "I didn't hear anything. Try again.")
    return {"heard": heard, **translate_cached(heard, lang)}


def lookup_lessons(lang: str) -> list:
    return lessons_of(lang) + word_items(lang) + localize(lang, rel_of(lang))["call_extras"]


def check_lang(lang: str) -> dict:
    if lang not in CONTENT:
        raise HTTPException(400, "Unsupported language")
    return {**localize(lang, rel_of(lang)), "lessons": lessons_of(lang), "tracks": tracks(lang)}


@app.get("/api/content")
def content():
    merged = {lang: check_lang(lang) for lang in CONTENT}
    return {"mock": gnani.is_mock(), "content": merged, "progress": load_progress(), "usage": gnani.usage()}


class Custom(BaseModel):
    lang: str
    ask: str
    target: str
    ask_roman: str = ""
    target_roman: str = ""
    target_en: str = ""


@app.post("/api/custom")
def add_custom(body: Custom):
    """A parent adds a family phrase. Parents write it, so it is spoken as typed."""
    check_lang(body.lang)
    fields = {k: v.strip()[:120] for k, v in body.model_dump().items() if k != "lang"}
    if not fields["ask"] or not fields["target"]:
        raise HTTPException(400, "Please fill in the question and the answer")
    item = {
        "id": "fam-" + hashlib.sha1(f"{fields['ask']}|{fields['target']}".encode()).hexdigest()[:8],
        "title": fields["target_en"] or "Family phrase",
        "ask_en": "", "target_en": fields["target_en"], "family": True,
        "ask": fields["ask"], "ask_roman": fields["ask_roman"],
        "target": fields["target"], "target_roman": fields["target_roman"] or fields["target"],
    }
    custom = load_custom()
    items = [x for x in custom.get(body.lang, []) if x["id"] != item["id"]]
    custom[body.lang] = (items + [item])[-12:]
    DATA.mkdir(parents=True, exist_ok=True)
    CUSTOM.write_text(json.dumps(custom, ensure_ascii=False, indent=1))
    return item


@app.delete("/api/custom/{lang}/{item_id}")
def delete_custom(lang: str, item_id: str):
    custom = load_custom()
    custom[lang] = [x for x in custom.get(lang, []) if x["id"] != item_id]
    CUSTOM.write_text(json.dumps(custom, ensure_ascii=False, indent=1))
    return {"ok": True}


class Line(BaseModel):
    lang: str
    key: str


def audio_for(lang: str, key: str) -> dict:
    check_lang(lang)
    try:
        if key.startswith("tr:"):
            text = load_translations()[key[3:]]["native"]
        elif key.startswith("chat:"):
            text = load_translations()[key[5:]]["native"]
        elif key == "greet":
            if not child_name():
                raise KeyError(key)
            text = GREET_FRAME[lang].format(name=child_name())
        else:
            text = line_text(lang, key, lookup_lessons(lang), rel_of(lang))
    except (KeyError, StopIteration, IndexError, ValueError):
        raise HTTPException(404, "Unknown line")
    voice = os.getenv("BEBE_VOICE", "Lakshmi")
    if key.startswith(("q:", "chat:")) and localize(lang, rel_of(lang))["relative"]["gender"] == "m":
        # In the pretend call a male relative's questions use a male voice; Taara keeps hers.
        voice = os.getenv("MALE_RELATIVE_VOICE", "Yashraj")
    mode = "mock" if gnani.is_mock() else "live"
    speed = gnani.speed()
    # The speed is part of the cache name, so changing it makes fresh audio instead of reusing old clips.
    tag = f"{voice}@{speed}-calm"
    name = hashlib.sha1(f"{mode}|{tag}|{lang}|{text}".encode()).hexdigest() + ".wav"
    path = AUDIO / name
    cached = path.exists()
    if not cached:
        if not text:
            raise HTTPException(404, "Nothing to say")
        # Exclamation marks make Timbre sound excited; a full stop keeps the voice calm and gentle.
        spoken = text.replace("!", "।" if not key.startswith("en:") else ".")
        audio = gnani.speak_timbre(spoken, "en-IN" if key.startswith("en:") else lang, voice)
        AUDIO.mkdir(parents=True, exist_ok=True)
        path.write_bytes(audio)
    return {"url": f"/audio/{name}", "cached": cached}


@app.post("/api/line")
def line(body: Line):
    return audio_for(body.lang, body.key)


class Lang(BaseModel):
    lang: str


@app.post("/api/prepare")
def prepare(body: Lang):
    """Make every fixed line once, so lessons play instantly and never cost again."""
    keys = all_keys(body.lang, lessons_of(body.lang), rel_of(body.lang))
    made = sum(0 if audio_for(body.lang, key)["cached"] else 1 for key in keys)
    return {"made": made, "total": len(keys)}


@app.post("/api/answer")
async def answer(audio: UploadFile = File(...), lang: str = Form(...), lesson_id: str = Form(...), mode: str = Form("lesson"), tr_id: str = Form("")):
    content_for = check_lang(lang)
    lesson = next((item for item in lookup_lessons(lang) if item["id"] == lesson_id), None)
    if tr_id:
        item = load_translations().get(tr_id)
        if not item:
            raise HTTPException(404, "Unknown translation")
        base = lesson or {"ask": item["english"], "ask_roman": ""}
        lesson = {**base, "id": lesson_id, "target": item["native"], "target_roman": item["roman"]}
    if not lesson:
        raise HTTPException(404, "Unknown lesson")
    wav = await audio.read()
    if len(wav) > 5 * 1024 * 1024 or audio_utils.duration(wav) > 20:
        raise HTTPException(400, "Answer too long")
    if audio_utils.is_silent(wav, threshold=150):
        return {"heard": "", "label": "silent"}
    keyterms = list(lesson["target"].split()) + [content_for["elder"]]
    heard = gnani.transcribe(wav, lang, keyterms)["transcript"].strip()
    if not heard:
        return {"heard": "", "label": "silent"}
    result = grade(heard, lesson, content_for["language_name"])

    progress = load_progress()
    key = f"{lang}:{lesson_id}"
    if RANK.get(result["label"], 0) > RANK.get(progress["lessons"].get(key), 0):
        progress["lessons"][key] = result["label"]
    progress["log"] = (progress["log"] + [{
        "at": datetime.now(timezone.utc).isoformat(), "lang": lang, "lesson": lesson_id,
        "mode": mode, "heard": heard, **result,
    }])[-200:]
    save_progress(progress)
    return {"heard": heard, **result}


@app.post("/api/call-done")
def call_done(body: Lang):
    check_lang(body.lang)
    progress = load_progress()
    progress["calls_done"][body.lang] = progress["calls_done"].get(body.lang, 0) + 1
    save_progress(progress)
    return progress


class Score(BaseModel):
    lang: str
    lesson_id: str = ""
    stars: int = 0
    xp: int = 0
    streak: int = 0


@app.post("/api/score")
def score(body: Score):
    """Game state: XP, stars per phrase, best streak, daily goal and badges."""
    check_lang(body.lang)
    progress = load_progress()
    game = progress["game"]
    game["xp"] += max(0, min(body.xp, 25))
    game["best_streak"] = max(game["best_streak"], body.streak)
    today = datetime.now(timezone.utc).date().isoformat()
    if game["today"]["date"] != today:
        game["today"] = {"date": today, "count": 0}
    if body.lesson_id and body.stars:
        key = f"{body.lang}:{body.lesson_id}"
        game["stars"][key] = max(game["stars"].get(key, 0), max(1, min(body.stars, 3)))
        game["today"]["count"] += 1
    core = [lesson["id"] for lesson in CONTENT[body.lang]["lessons"]]
    earned = {
        "first": bool(game["stars"]),
        "streak3": game["best_streak"] >= 3,
        "call": any(progress["calls_done"].values()),
        "all": all(game["stars"].get(f"{body.lang}:{i}") for i in core),
    }
    game["badges"] = [name for name, ok in earned.items() if ok]
    save_progress(progress)
    return progress


@app.post("/api/reset")
def reset():
    if PROGRESS.exists():
        PROGRESS.unlink()
    return {"ok": True}


@app.get("/audio/{name}")
def audio_file(name: str):
    path = (AUDIO / name).resolve()
    if path.parent != AUDIO.resolve() or path.suffix != ".wav" or not path.exists():
        raise HTTPException(404)
    return FileResponse(path, media_type="audio/wav")


app.mount("/", StaticFiles(directory=ROOT / "static", html=True), name="static")
