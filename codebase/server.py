from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
load_dotenv(PROJECT_ROOT / ".env")

from cp3_core import (
    DEFAULT_MODEL,
    MissingApiKeyError,
    answer_question,
    load_sources,
    result_to_dict,
    safe_error_text,
)


app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify(
        {
            "ok": True,
            "model": DEFAULT_MODEL,
            "source_count": len(load_sources()),
        }
    )


@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return (
            jsonify(
                {
                    "error": "Bạn chưa nhập câu hỏi.",
                    "decision": "VALIDATION_ERROR",
                    "answer": "Hãy nhập một câu hỏi về bài học của khóa AI20k.",
                    "source_ids": [],
                }
            ),
            400,
        )

    try:
        result = answer_question(question)
        response = result_to_dict(result)
        response.pop("raw_text", None)
        return jsonify(response)
    except MissingApiKeyError as exc:
        app.logger.error("Gemini configuration error: %s", safe_error_text(exc))
        return (
            jsonify(
                {
                    "error": "GEMINI_API_KEY is not configured.",
                    "decision": "CONFIG_ERROR",
                    "answer": "Backend chưa có GEMINI_API_KEY nên chưa thể gọi AI thật.",
                    "source_ids": [],
                }
            ),
            503,
        )
    except Exception as exc:
        app.logger.exception("Gemini pipeline error: %s", safe_error_text(exc))
        return (
            jsonify(
                {
                    "error": "Gemini pipeline failed.",
                    "decision": "BACKEND_ERROR",
                    "answer": "Backend gặp lỗi khi gọi AI. Vui lòng kiểm tra terminal và trace.",
                    "source_ids": [],
                }
            ),
            502,
        )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
