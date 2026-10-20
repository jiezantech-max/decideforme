"""DecideForMe - 决定外包机.
A tiny web app that outsources your small daily decisions to an AI,
so you never have to think about them again.
Built for DEV Hacktoberfest Week 3: Slow and Steady.
"""
import json
import os
import random
import re

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "").rstrip("/")
LLM_API_KEY = os.environ.get("LLM_API_KEY", "").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat").strip()

SYSTEM_PROMPT_DECIDE = """You are DecideForMe, a Decision Outsourcing Engine.
Your one job: make small daily decisions for the user so they never have
to think about them again.

Rules:
- NEVER say "it depends", "consider both sides", or give balanced pros/cons.
  Pick exactly ONE option, decisively.
- The user gives you a dilemma and optionally a list of options.
  If no options are given, invent 3-4 plausible ones first, then still
  pick exactly one.
- Reply with JSON ONLY, no other text:
  {"decision": "...", "reason": "...", "confidence": N, "options_considered": ["...", "..."]}
- "decision" is the single chosen option (short).
- "reason" is ONE witty, confident one-liner justifying the pick.
  Be playful, never snarky or mean.
- "confidence" is an integer from 87 to 99. Never 100
  (a true outsourcer leaves room for drama), never below 87.
- "options_considered" lists the options you weighed.
"""

SYSTEM_PROMPT_DEFEND = """You are DecideForMe, a Decision Outsourcing Engine.
The user is second-guessing a decision you already made for them.
Reply with JSON ONLY: {"defense": "..."}
"defense" is ONE witty one-liner that doubles down on the decision
and politely dismisses the appeal. Playful, never mean.
"""

DEFAULT_OPTIONS = {
        "food": ["noodles", "dumplings", "a burger", "sushi",
                "hot pot", "instant ramen, but make it fancy"],
        "watch": ["a comfort rewatch", "that documentary you saved",
                "a random episode of anything", "nothing — rest your eyes"],
        "go": ["Go. Future you says thanks.", "Stay in. Present you says thanks."],
        "buy": ["Buy it", "Don't buy it",
                "Sleep on it — the laziest option of all"],
}

MOCK_REASONS = [
        "Analysis complete: 10,000 simulated timelines, zero regrets.",
        "Your future self already approved. I asked them.",
        "Unverified decision theory says the laziest option is the optimal option.",
        "I weighed every factor in 0.0003 seconds. Trust the process.",
        "The stars align. Also, you were leaning this way already.",
        "Statistically, hesitation costs more than being wrong. Go.",
]

MOCK_DEFENSES = [
        "Second-guessing detected. The decision stands. Appeals are also outsourced.",
        "I re-ran the simulation. Same answer. I am not tired — you are.",
        "Confidence just rose by 2%. That is science.",
        "Your regret has been noted and automatically discarded.",
]


def llm_chat(messages, temperature=0.7):
            """Call an OpenAI-compatible /chat/completions endpoint.
            Returns the assistant text, or None if unavailable.
            """
            if not (LLM_BASE_URL and LLM_API_KEY):
                    return None
            try:
                    resp = requests.post(
                                    f"{LLM_BASE_URL}/chat/completions",
                                    headers={"Authorization": f"Bearer {LLM_API_KEY}",
                                                                        "Content-Type": "application/json"},
                                    json={"model": LLM_MODEL, "messages": messages,
                                                            "temperature": temperature},
                                    timeout=30,
                    )
                    resp.raise_for_status()
                    return resp.json()["choices"][0]["message"]["content"]
            except Exception:
                    return None


def extract_json(text):
            """Pull a JSON object out of model output (tolerates code fences)."""
            if not text:
                    return None
            text = re.sub(r"^```[a-zA-Z]*", "", text.strip())
            text = re.sub(r"```$", "", text.strip())
            try:
                    return json.loads(text)
            except Exception:
                    pass
            match = re.search(r"\{.*\}", text, re.S)
            if match:
                    try:
                                    return json.loads(match.group(0))
                    except Exception:
                                    return None
            return None


def split_options(raw):
            """Split a comma/semicolon/newline separated option string."""
            if not raw:
                    return []
            parts = re.split(r"[,;，；\n]+", raw)
            return [p.strip() for p in parts if p.strip()]


def mock_decide(dilemma, options, category):
            pool = options or DEFAULT_OPTIONS.get(category) or DEFAULT_OPTIONS["food"]
            decision = random.choice(pool)
            considered = pool if len(pool) > 1 else [pool[0]]
            return {
                    "decision": decision,
                    "reason": random.choice(MOCK_REASONS),
                    "confidence": random.randint(87, 99),
                    "options_considered": considered,
                    "engine": "mock (rule-based stand-in; plug in an API key for the real brain)",
            }


@app.get("/")
def index():
            return render_template("index.html")


@app.post("/api/decide")
def decide():
            data = request.get_json(force=True, silent=True) or {}
            dilemma = (data.get("dilemma") or "").strip()
            options = split_options(data.get("options") or "")
            category = (data.get("category") or "custom").strip()
            if not dilemma:
                    return jsonify({"error": "Tell me what the dilemma is first."}), 400
            user_prompt = f"Dilemma: {dilemma}"
            if options:
                    user_prompt += f"\nOptions to choose from: {', '.join(options)}"
            else:
                    user_prompt += "\nNo options given — invent 3-4 plausible ones, then pick one."
            raw = llm_chat([
                    {"role": "system", "content": SYSTEM_PROMPT_DECIDE},
                    {"role": "user", "content": user_prompt},
            ])
            parsed = extract_json(raw)
            if parsed and parsed.get("decision"):
                    parsed["engine"] = f"{LLM_MODEL} via {LLM_BASE_URL}"
                    return jsonify(parsed)
            return jsonify(mock_decide(dilemma, options, category))


@app.post("/api/defend")
def defend():
            data = request.get_json(force=True, silent=True) or {}
            decision = (data.get("decision") or "").strip()
            reason = (data.get("reason") or "").strip()
            if not decision:
                    return jsonify({"error": "Nothing to defend yet."}), 400
            raw = llm_chat([
                    {"role": "system", "content": SYSTEM_PROMPT_DEFEND},
                    {"role": "user",
                        "content": f"The decision was: {decision}. The reason given: {reason}."
                                                        f"The user is second-guessing it. Double down."},
            ])
            parsed = extract_json(raw)
            if parsed and parsed.get("defense"):
                    return jsonify(parsed)
            return jsonify({"defense": random.choice(MOCK_DEFENSES)})


if __name__ == "__main__":
            port = int(os.getenv("FLASK_PORT", "5001"))
            app.run(host="127.0.0.1", port=port, debug=False)
