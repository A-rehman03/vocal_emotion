import os
import tempfile

import numpy as np
import torch
import torch.nn.functional as F
from flask import Flask, jsonify, render_template, request
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

from utils.audio_utils import load_audio_as_np

app = Flask(__name__)

# Model selection
MODEL_NAME = "prithivMLmods/Speech-Emotion-Classification"
device = 0 if torch.cuda.is_available() else -1

# Load once at startup
extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)
model.eval()
if device >= 0:
    model.to("cuda")

# All emotion labels
LABELS = [model.config.id2label[i] for i in range(len(model.config.id2label))]


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
        # Load and resample
        audio_np, sr = load_audio_as_np(tmp_path, target_sr=16000)
        inputs = extractor(audio_np, sampling_rate=sr, return_tensors="pt")
        if device >= 0:
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        with torch.no_grad():
            logits = model(**inputs).logits
        probs = F.softmax(logits, dim=-1)[0].cpu().numpy()

        # Build prediction list
        preds = [
            {"label": LABELS[i], "score": float(probs[i])} for i in range(len(LABELS))
        ]
        preds = sorted(preds, key=lambda x: x["score"], reverse=True)
        return jsonify({"predictions": preds})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
