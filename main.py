from flask import Flask, request, jsonify
from flask_cors import CORS

from query import ask_llm_answer
from setting import get_logger

logger = get_logger(__name__)

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("question", "").strip()

    if not question:
        return jsonify({"error": "question is required"}), 400

    try:
        answer = ask_llm_answer(question)
        return jsonify({
            "question": question,
            "answer": answer
        })
    except Exception:
        logger.exception("Failed to answer question")
        return jsonify({"error": "Failed to answer question"}), 500
