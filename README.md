# Taara – Aapki India Se Dost

Taara helps kids who grow up abroad (ages 2 to 10) learn Hindi and Punjabi, so they can actually talk to their Dadi, Nani, Dada and the rest of the family on the phone.

Built solo by Sunit Singh Dhaliwal for Gnani AI's Great Indian AI Internship Challenge.
#GnaniAI #GreatIndianAIInternshipChallenge

## What it does

- **Pretend call (main feature).** The child picks a relative and just talks. Taara plays that relative in simple Hindi or Punjabi. If the child answers in English, Taara shows the Hindi way to say it, the child says it back, and the call carries on. Male relatives (Dada, Nana, Chacha, Mama) get a male voice.
- **Practice call.** The questions relatives always ask (have you eaten, how is school, when are you coming to India), plus two questions special to each relative.
- **Phrase lessons.** Stars, XP, levels, streaks and a build-the-sentence game. Word-by-word feedback shows which words were right.
- **First words.** 9 sets of about 50 words (family, food, numbers, colours, animals, body, feelings, kind words).
- **Little ones (2 to 4).** Tap games with no speaking needed: Listen and learn, Find the colour, Count with Taara.
- **Say it in Hindi / Punjabi.** Type or say anything in English and Taara gives a short, child-friendly version, then the child practises saying it.
- **Voice message** to send to a relative, and a **quick quiz**.
- **For parents.** Child's name and gender (for correct Hindi/Punjabi verb forms), progress, badges, a WhatsApp summary for family, and family phrases parents can add themselves.

Taara is a coach, not a relative. Pretend calls are clearly labelled as a game, and every session ends by pointing the child to a real call.

## Gnani AI models used

| Job | Gnani model | Endpoint |
|---|---|---|
| Hearing the child (Hindi or Punjabi, plus English) | **Prisma v3.0** speech to text | `POST https://api.vachana.ai/stt/v3` |
| Taara's and the relatives' voices | **Timbre v3.0** text to speech, voices Lakshmi (female) and Yashraj (male), speed 0.85 for a calm voice | `POST https://api.vachana.ai/api/v1/tts/inference` |

I also tried Gnani voice cloning (`vachana-vc-v1`) on my own voice for an early version of the demo narration. It isn't part of the app.

Other model: Groq `openai/gpt-oss-120b` writes the pretend-call replies, the English to Hindi/Punjabi translations and labels unclear answers. Its output is checked before a child hears it: it must be in the right script, short, child-safe, and it never asks for personal details.

## How it's built

- `server.py`: FastAPI backend. Every fixed line is spoken once with Timbre and cached on disk, so lessons replay for free. Silence is never sent to Prisma, and the app stops at `MAX_LIVE_GNANI_CALLS`.
- `lessons.py`: all lessons, questions per relative, word sets and Taara's lines, written by hand for Hindi and Punjabi.
- `grade.py`: fuzzy matching first, then the LLM only for unclear answers. It catches English even when Prisma writes it in Hindi letters ("आई फाइन").
- `chat.py`: pretend-call replies with guardrails.
- `translate.py`: guarded English to Hindi/Punjabi translation.
- `gnani.py`: Prisma and Timbre calls, mock mode and the credit guard.
- `static/`: one web page (HTML, CSS, JS). No framework.

## Run it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # add your Gnani and Groq keys
.venv/bin/python -m uvicorn server:app --port 8000
```

Open http://localhost:8000 in Chrome and allow the microphone. Set `MOCK_GNANI=1` to try it with beeps and no API calls. Tests: `.venv/bin/pytest -q`.

## Limits

- Prisma is tuned mostly for adult speech, so very young children may be misheard. Grading is generous on purpose.
- Not yet tested with real children. In the demo, the child's answers are an AI voice.
- It doesn't grade pronunciation, and the pretend-call replies come from an LLM, so they vary from call to call.
