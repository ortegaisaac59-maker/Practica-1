
import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = os.getenv("HF_MODEL", "nlptown/bert-base-multilingual-uncased-sentiment")

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/sentiment")
def api_sentiment():
    if not HUGGINGFACE_API_KEY:
        return jsonify({"ok": False, "error": "Falta HUGGINGFACE_API_KEY en variables de entorno."}), 500

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"ok": False, "error": "Texto vacío."}), 400

    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        resp = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json={"inputs": text},
            timeout=30
        )
        if resp.status_code != 200:
            return jsonify({"ok": False, "error": f"Error en HuggingFace: {resp.status_code} {resp.text}"}), 502

        hf = resp.json()
        # Expected format varies by model. For nlptown/... it's list of list of dicts with labels 1-5 stars.
        # Let's normalize to a simple {label, score} with stars.
        label = None
        score = None
        if isinstance(hf, list) and hf and isinstance(hf[0], list):
            # pick max
            best = max(hf[0], key=lambda x: x.get("score", 0))
            label = best.get("label")
            score = float(best.get("score", 0))
        elif isinstance(hf, list) and hf and isinstance(hf[0], dict):
            best = max(hf, key=lambda x: x.get("score", 0))
            label = best.get("label")
            score = float(best.get("score", 0))
        else:
            label = "unknown"
            score = 0.0

        # Map label to sentiment category when possible
        sentiment = "neutral"
        if label:
            low = label.lower()
            if "1" in low or "negative" in low or "neg" in low:
                sentiment = "negative"
            elif "5" in low or "positive" in low or "pos" in low:
                sentiment = "positive"
            elif "4" in low:
                sentiment = "positive"
            elif "2" in low:
                sentiment = "negative"
            elif "3" in low or "neutral" in low:
                sentiment = "neutral"

        return jsonify({"ok": True, "model": HF_MODEL, "label": label, "sentiment": sentiment, "confidence": round(score, 4)}), 200

    except requests.Timeout:
        return jsonify({"ok": False, "error": "Tiempo de espera agotado al consultar la API."}), 504
    except Exception as e:
        return jsonify({"ok": False, "error": f"Excepción: {e}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
