import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from groq import Groq

load_dotenv()

app = Flask(__name__)

HISTORY_FILE = Path(__file__).parent / "history.json"
MAX_HISTORY = 10

SYSTEM_PROMPT = """You are an expert freelance consultant who analyzes job postings and writes winning proposals.

Given a freelance job description, respond with a JSON object containing exactly these keys:
- "project_summary": A concise 2-4 sentence overview of what the client needs.
- "complexity_score": An integer from 1 (trivial) to 10 (highly complex).
- "budget_range": A realistic estimated budget range in USD (e.g. "$2,000 – $4,500").
- "timeline": A realistic estimated delivery timeline (e.g. "3–4 weeks").
- "proposal": A polished, professional proposal letter (3-5 paragraphs) tailored to the job. Write in first person, be specific, highlight relevant expertise, and include a brief approach.
- "questions_for_client": An array of 3-5 thoughtful clarifying questions to ask the client before starting.

Base estimates on typical freelance market rates. Be honest about complexity. Return only valid JSON, no markdown fences."""


def get_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    return Groq(api_key=api_key)


def load_history() -> list:
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history: list) -> None:
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[:MAX_HISTORY], f, indent=2, ensure_ascii=False)


def save_analysis(job_description: str, result: dict) -> dict:
    entry = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "job_description": job_description,
        **result,
    }
    history = load_history()
    history.insert(0, entry)
    save_history(history)
    return entry


def history_summaries() -> list:
    summaries = []
    for entry in load_history()[:MAX_HISTORY]:
        summary = entry.get("project_summary", "")
        preview = summary[:80] + "..." if len(summary) > 80 else summary
        summaries.append({
            "id": entry["id"],
            "created_at": entry["created_at"],
            "preview": preview or "Untitled analysis",
            "complexity_score": entry.get("complexity_score"),
            "budget_range": entry.get("budget_range"),
        })
    return summaries


def get_analysis(entry_id: str) -> dict | None:
    for entry in load_history():
        if entry.get("id") == entry_id:
            return entry
    return None


def normalize_result(result: dict) -> dict:
    required_keys = {
        "project_summary",
        "complexity_score",
        "budget_range",
        "timeline",
        "proposal",
        "questions_for_client",
    }
    if not required_keys.issubset(result.keys()):
        missing = required_keys - result.keys()
        raise ValueError(f"Incomplete AI response. Missing: {', '.join(missing)}")

    score = result["complexity_score"]
    if not isinstance(score, int) or not 1 <= score <= 10:
        try:
            score = int(round(float(score)))
            score = max(1, min(10, score))
        except (TypeError, ValueError):
            score = 5
        result["complexity_score"] = score

    if not isinstance(result["questions_for_client"], list):
        result["questions_for_client"] = [str(result["questions_for_client"])]

    return result


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/history")
def history_list():
    return jsonify(history_summaries())


@app.route("/history/<entry_id>")
def history_detail(entry_id):
    entry = get_analysis(entry_id)
    if not entry:
        return jsonify({"error": "Analysis not found."}), 404
    return jsonify(entry)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    job_description = (data.get("job_description") or "").strip()

    if not job_description:
        return jsonify({"error": "Please provide a job description."}), 400

    if len(job_description) > 15000:
        return jsonify({"error": "Job description is too long (max 15,000 characters)."}), 400

    try:
        client = get_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Analyze this freelance job posting and generate a proposal:\n\n{job_description}",
                },
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        result = normalize_result(json.loads(content))
        entry = save_analysis(job_description, result)

        return jsonify({
            **result,
            "id": entry["id"],
            "job_description": job_description,
        })

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response. Please try again."}), 502
    except Exception as exc:
        message = str(exc)
        if "api_key" in message.lower() or "authentication" in message.lower():
            return jsonify({"error": "Invalid or missing Groq API key."}), 401
        return jsonify({"error": f"Generation failed: {message}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
