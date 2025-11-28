"""
Simple Speech Emotion Recognition Flask API
Minimal dependencies version
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Emotion labels
CLASS_LABELS = [
    "Neutral", "Calm", "Happy", "Sad", "Angry", "Fearful", "Disgust", "Surprised"
]

# Simple emoji mapping
EMOTION_EMOJIS = {
    'Neutral': 'neutral',
    'Calm': 'calm', 
    'Happy': 'happy',
    'Sad': 'sad',
    'Angry': 'angry',
    'Fearful': 'fearful',
    'Disgust': 'disgust',
    'Surprised': 'surprised'
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": True,
        "model_path": "simple_mock_model",
        "supported_emotions": CLASS_LABELS,
        "emotion_emojis": EMOTION_EMOJIS
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Mock prediction endpoint for testing"""
    if 'audio' not in request.files:
        return jsonify({"error": "Missing 'audio' file in form-data"}), 400

    file = request.files['audio']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check file size (limit to 10MB)
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > 10 * 1024 * 1024:
        return jsonify({"error": "File too large. Maximum size is 10MB"}), 400
    
    if file_size == 0:
        return jsonify({"error": "Empty file"}), 400

    try:
        # Mock prediction for testing
        import random
        
        # Simulate processing time
        import time
        time.sleep(0.5)
        
        # Random emotion prediction for testing
        predicted_emotion = random.choice(CLASS_LABELS)
        confidence = round(random.uniform(0.6, 0.95), 3)
        
        # Generate mock probabilities
        probabilities = [round(random.uniform(0.01, 0.3), 3) for _ in CLASS_LABELS]
        emotion_index = CLASS_LABELS.index(predicted_emotion)
        probabilities[emotion_index] = confidence
        
        # Normalize probabilities
        total = sum(probabilities)
        probabilities = [round(p/total, 3) for p in probabilities]
        
        emotion_probs = {emotion: float(prob) for emotion, prob in zip(CLASS_LABELS, probabilities)}
        
        response = {
            "predicted_emotion": predicted_emotion,
            "emoji": EMOTION_EMOJIS[predicted_emotion],
            "confidence": confidence,
            "all_probabilities": emotion_probs,
            "raw_prediction": probabilities,
            "input_shape": [1, 180, 1],
            "audio_info": {
                "duration": round(file_size / 44100, 2),  # Rough estimate
                "sample_rate": 22050,
                "channels": 1
            }
        }

        return jsonify(response), 200
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({"error": f"Audio processing failed: {str(e)}"}), 500

@app.route('/emotions', methods=['GET'])
def get_emotions():
    """Get list of supported emotions with emojis"""
    return jsonify({
        "emotions": CLASS_LABELS,
        "emojis": EMOTION_EMOJIS
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5001'))
    print(f"Starting Simple Speech Emotion Recognition API on port {port}")
    print(f"Model loaded: True (Mock)")
    print(f"Supported emotions: {CLASS_LABELS}")
    app.run(host='0.0.0.0', port=port, debug=True)

