# DEV Week 3 投稿文（最终版，可直接发）

> 发帖步骤（5 分钟）：
> 1. 登录 dev.to（没有账号先注册一个）
> 2. 打开官方预填模板链接（见下，tags devchallenge + hf26challenge 和 8 个章节标题已自动填好）
> 3. 标题栏填：I built a machine that decides so I don't have to 🦥
> 4. 把下方正文逐节粘贴进对应章节，删掉模板里的 HTML 注释
> 5. **删掉 "My Agent Session" 和 "Prize Categories" 两个章节**（没用 DevRelay、没领 .tech）
> 6. 点 Publish
>
> 模板链接：
> https://dev.to/new?prefill=---%0Atitle%3A%20%0Apublished%3A%20%0Atags%3A%20devchallenge%2C%20hf26challenge%0A---%0A%0A%2AThis%20is%20a%20submission%20for%20the%20%5BHacktoberfest%20Open-Source%20AI%20Challenge%20Week%203%3A%20Slow%20and%20Steady%5D%28https%3A%2F%2Fdev.to%2Fchallenges%2Fhacktoberfest-week3-2026-10-19%29%2A%0A%0A%23%23%20What%20I%20Built%0A%3C%21--%20What%20does%20it%20do%2C%20and%20what%20effort%20does%20it%20save%3F%20Who%20gets%20to%20be%20a%20little%20lazier%20because%20of%20it%3F%20--%3E%0A%0A%23%23%20Demo%0A%3C%21--%20Share%20a%20deployed%20link%20or%20a%20video%20demo.%20--%3E%0A%0A%23%23%20Code%0A%3C%21--%20Show%20us%20the%20code%21%20%20You%20can%20embed%20a%20GitHub%20repo%20directly%20into%20your%20post.%20--%3E%0A%0A%23%23%20How%20I%20Built%20It%0A%3C%21--%20Which%20open-source%20AI%20did%20you%20use%20%28open-weight%20models%2C%20agent%20harnesses%2C%20frameworks%2C%20local%20inference%29%2C%20and%20how%20is%20your%20project%20built%20around%20it%3F%20--%3E%0A%0A%23%23%20Why%20Does%20Open%20Innovation%20Matter%3F%0A%3C%21--%20Why%20does%20open%20innovation%20matter%20for%20what%20you%20built%3F%20%20What%20did%20it%20make%20possible%20that%20a%20closed%20API%20wouldn%27t%3F%20--%3E%0A%0A%23%23%20My%20Agent%20Session%0A%3C%21--%20Optional%2C%20but%20judges%20love%20it.%20%20Save%20your%20session%20with%20DevRelay%20and%20embed%20it%20with%20the%20agent_session%20tag%20%28see%20the%20challenge%20page%29%2C%20or%20link%20to%20it.%20--%3E%0A%0A%23%23%20The%20Lazy%20Payoff%0A%3C%21--%20Optional%2C%20but%20this%20is%20where%20you%20can%20make%20your%20post%20stand%20out.%20%20How%20much%20time%20or%20effort%20does%20it%20actually%20save%3F%20%20Did%20you%20%28or%20someone%20else%29%20use%20it%20this%20week%3F%20%20If%20not%2C%20remove%20this%20section.%20--%3E%0A%0A%23%23%20Prize%20Categories%0A%3C%21--%20Which%20partner%20categories%20are%20you%20entering%3F%20%20List%20every%20one%20that%20applies%2C%20or%20remove%20this%20section.%20--%3E%0A%0A%3C%21--%20Team%20Submissions%3A%20Please%20pick%20one%20member%20to%20publish%20the%20submission%20and%20credit%20teammates%20by%20listing%20their%20DEV%20usernames%20directly%20in%20the%20body%20of%20the%20post.%20--%3E%0A%0A%3C%21--%20Thanks%20for%20participating%21%20--%3E%0A
>
> 截止：北京时间 2026-10-26 14:59（PDT 10-25 23:59）。

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

Live demo: https://decide.motinextai.com — the Decision Outsource Machine
on my own domain via Cloudflare Tunnel. Prefer local? `python app.py` →
http://localhost:5001 (mock mode needs no API key).

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
