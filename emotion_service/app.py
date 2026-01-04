import os
import tempfile
import gc

import numpy as np
import torch
import torch.nn.functional as F
from flask import Flask, jsonify, render_template, request
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

from utils.audio_utils import load_audio_as_np

app = Flask(__name__)

# Model Configuration
MODEL_ROOT = os.path.join(os.path.dirname(__file__), "model")
# Default model name if local path doesn't exist
DEFAULT_MODEL_NAME = "prithivMLmods/Speech-Emotion-Classification"

def get_model_path():
    """Resolve the correct model path dynamically."""
    ref_path = os.path.join(MODEL_ROOT, "refs", "main")
    if os.path.exists(ref_path):
        with open(ref_path, "r") as f:
            commit_hash = f.read().strip()
        return os.path.join(MODEL_ROOT, "snapshots", commit_hash)
    elif os.path.exists(os.path.join(MODEL_ROOT, "config.json")):
        return MODEL_ROOT
    return DEFAULT_MODEL_NAME

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    f = request.files["audio"]
    if f.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save temp file
    suffix = os.path.splitext(f.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp_path = tmp.name
        f.save(tmp_path)

    try:
        # Load and resample audio first (lightweight)
        audio_np, sr = load_audio_as_np(tmp_path, target_sr=16000)
        
        # LAZY LOAD MODEL (Only when needed)
        # This prevents the app from idling with >500MB RAM usage
        model_name = get_model_path()
        
        extractor = AutoFeatureExtractor.from_pretrained(model_name)
        model = AutoModelForAudioClassification.from_pretrained(model_name)
        model.eval()
        
        # Optimize for CPU (Render Free Tier has no GPU usually)
        device = "cpu"
        model.to(device)

        inputs = extractor(audio_np, sampling_rate=sr, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            logits = model(**inputs).logits
        probs = F.softmax(logits, dim=-1)[0].cpu().numpy()

        # Build prediction list
        LABELS = [model.config.id2label[i] for i in range(len(model.config.id2label))]
        LABEL_MAP = {
            "DIS": "Disgust", "ANG": "Anger", "SAD": "Sadness",
            "HAP": "Happiness", "NEU": "Neutral", "SUR": "Surprise",
            "CAL": "Calm", "FEA": "Fear"
        }
        
        preds = [
            {"label": LABEL_MAP.get(LABELS[i], LABELS[i]), "score": float(probs[i])}
            for i in range(len(LABELS))
        ]
        preds = sorted(preds, key=lambda x: x["score"], reverse=True)
        
        # CLEANUP: Delete model to free RAM immediately
        del model
        del extractor
        del inputs
        del logits
        gc.collect()  # Force garbage collection
        
        return jsonify({"predictions": preds})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # File cleanup
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

if __name__ == "__main__":
    # Use PORT env variable if available (Render), otherwise fallback to 5002 (Local)
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)
