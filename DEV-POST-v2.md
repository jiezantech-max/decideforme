# DEV Week 3 投稿文（英文 · 按官方模板改写）

> 投稿步骤：登录 dev.to → 打开官方预填模板链接
> （链接很长，从 https://dev.to/new?prefill= 开始——模板会自动填好标签 devchallenge + hf26challenge
> 和 8 个章节标题）
>
> → 把下方正文逐节粘贴进对应章节，删掉模板里的 HTML 注释，把 [待填] 换成你的链接后点 Publish。
> 截止：北京时间 2026-10-26 14:59（PDT 10-25 23:59）。
>
> 注意：投稿需要登录 dev.to 账号（他之前未确认有没有账号）。

---

# I built a machine that decides so I don't have to 🦥

Week 3's theme — *Slow and Steady* — hit a nerve. Not because I'm fast
and furious, but because I'm the opposite: I burn an embarrassing amount
of brainpower every day on decisions that don't matter. What to eat. What
to watch. Whether to go. Whether to buy. Tiny, forgettable choices, yet
each one charges a small tax of attention.

So I asked: **what if I could outsource decisions themselves?** Not the
execution — I can order food in three taps. The *deciding*. The part
where you stand in front of the fridge for six minutes, door open, like
a confused penguin.

## What I Built

**DecideForMe** — a decision outsourcing engine. You type your dilemma,
optionally throw in some options (or don't — the engine will invent them
for you, that's part of the laziness), and hit one big red button. Out
comes a verdict: one option, picked decisively, with a witty one-line
justification and a confidence score between 87% and 99%.

Never 100%. A true outsourcer leaves room for drama.

There's also a daily counter showing how many decisions you've outsourced
today, and a "Disagree?" button that lets you appeal the verdict — where
**The Defender** politely doubles down instead of re-deciding. ("Your
regret has been noted and automatically discarded.")

## Demo

Live demo (once the tunnel picks it up): https://decide.motinextai.com
— the Decision Outsource Machine on my own domain via Cloudflare Tunnel.
Prefer local? `python app.py` → http://localhost:5001 (mock mode needs no API key).

## Code

https://github.com/jiezantech-max/decideforme — public repo, MIT license.

## How I Built It

The whole brain is an **open-weight LLM** (default: DeepSeek) called
through an OpenAI-compatible API. Two carefully written system prompts
do all the work:

1. **The Decider** is explicitly forbidden from hedging. No "it depends",
   no balanced pros-and-cons. It must return JSON —
   `{decision, reason, confidence, options_considered}` — with exactly one
   winner.
2. **The Defender** handles appeals. Instead of re-deciding, it doubles
   down with a one-liner that politely dismisses your regret.

The app itself is a small Flask service with a playful single-page UI,
including a stamp animation ("OUTSOURCED ✓"). There's also a **mock
mode** — curated option pools and canned witty reasons — so the full
flow works with zero API key and a demo is one `python app.py` away.

## Why Does Open Innovation Matter?

The engine is built around the open model ecosystem, not a closed black
box. Because the brain is an open-weight LLM behind a standard
OpenAI-compatible interface, the app stays portable and cheap: swap in
any open model, run locally if you want, and never depend on a single
vendor's pricing or uptime. Mock mode even works fully offline. Open
innovation is what makes "outsourcing decisions" a toy anyone can run,
not a service someone has to rent.

## The Lazy Payoff

Before: 5 minutes of fridge-staring, 20 tabs of "best ramen near me"
reviews, one group chat poll that nobody answers.
After: type the dilemma, hit the button, 10 seconds, done — with a
confidence score high enough to blame.

I outsourced 14 decisions this week. I regret zero of them. The machine
didn't even let me regret them.

## Prize Categories

[可选：如果领了免费 .tech 域名并部署上线，写上 Best Use of a .tech Domain；
没领就直接删掉整个章节]
