# DEV submission post — DRAFT (English)

> Post this on dev.to with tags: #devchallenge #hf26challenge
> Deadline: 2026-10-26 14:59 CST (Beijing time)

---

# I built a machine that decides so I don't have to 🦥

Week 3's theme — *Slow and Steady* — hit a nerve. Not because I'm fast
and furious, but because I'm the opposite: I spend an embarrassing amount
of brainpower every day on decisions that don't matter. What to eat. What
to watch. Whether to go. Whether to buy. These are tiny, forgettable
choices, yet each one charges me a small tax of attention.

So I asked: **what if I could outsource decisions themselves?** Not the
execution — I can already order food in three taps. The *deciding*. The
part where you stand in front of the fridge for six minutes, door open,
like a confused penguin.

Meet **DecideForMe** — a decision outsourcing engine. You type your
dilemma, optionally throw in some options (or don't — the engine will
invent them for you, that's part of the laziness), and hit one big red
button. Out comes a verdict: one option, picked decisively, with a witty
one-line justification and a confidence score between 87% and 99%.

Never 100%. A true outsourcer leaves room for drama.

## How it works

The whole brain is an **open-weight LLM** called through an OpenAI-compatible
API. Two carefully written system prompts do all the work:

1. **The Decider** is explicitly forbidden from hedging. No "it depends",
   no balanced pros-and-cons. It must return JSON —
   `{decision, reason, confidence, options_considered}` — with exactly one
   winner.
2. **The Defender** kicks in when you hit the "Disagree?" button. Instead
   of re-deciding, it doubles down with a one-liner that politely
   dismisses your appeal. ("Your regret has been noted and automatically
   discarded.")

The app itself is a small Flask service with a playful single-page UI,
including a stamp animation ("OUTSOURCED ✓") and a daily counter of how
many decisions you've outsourced. There's also a mock mode — curated
option pools and canned witty reasons — so the full flow works without an
API key, and a demo is one `python app.py` away.

## Why slow and steady?

Decision fatigue research aside, this project's philosophy is pure sloth:
**thinking is the last unpaid labor.** Every "quick decision" you make
yourself is a context switch you didn't need. A sloth doesn't rush —
it conserves. DecideForMe is my attempt to make laziness a feature, not
a bug.

## Try it

- Repo: [link]
- Demo: [link]
- One command: `python app.py` → open http://localhost:5001

Go outsource something small today. Future you says thanks. 🦥
