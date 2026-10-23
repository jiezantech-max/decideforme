# DecideForMe · 决定外包机

> 把生活里的小纠结外包给 AI，大脑留给大事。Outsource your small decisions. Keep your brain for big ones.

Built for **DEV Hacktoberfest 2026 — Week 3: Slow and Steady**
(challenge prompt: build something with open-source AI at its core).

## What it does

Every day you burn mental energy on tiny decisions: what to eat, what to
watch, whether to go, whether to buy. DecideForMe outsources them to an AI
that **always picks one option decisively** — no "it depends", no pros/cons
list, just a verdict, a witty one-line justification, and a suspiciously
high confidence score (87–99%, never 100 — a true outsourcer leaves room
for drama).

Features:

- 🍜🎬🚶🛒 Category presets (food, watch, go-or-not, buy-or-not) + custom
- 💬 Give it options, or leave the field blank and the AI invents 3–4
- 🤔 "Disagree?" button — the engine doubles down and defends its decision
- 🦥 A daily counter: "Decisions outsourced today: N"

## How it works

A Flask backend calls an **OpenAI-compatible chat completions API**
running an **open-weight model** (default: DeepSeek). Two system prompts do
the magic:

- **Decider**: forced to output JSON `{decision, reason, confidence,
  options_considered}`, never hedging.
- **Defender**: a one-liner that doubles down when the user second-guesses.

Without an API key the app runs in **mock mode** (random pick from curated
option pools + witty canned reasons), so the whole flow is testable
without spending a cent.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your LLM API key, never commit .env
python app.py          # http://localhost:5001
```

## Configuration (.env)

| Key | Description |
|---|---|
| `LLM_BASE_URL` | OpenAI-compatible base URL, e.g. `https://api.deepseek.com` |
| `LLM_API_KEY` | Your API key |
| `LLM_MODEL` | Model name, e.g. `deepseek-chat` |
| `FLASK_PORT` | Port (default 5001) |

## License

MIT — see LICENSE.
