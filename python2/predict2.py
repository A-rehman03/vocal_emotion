"""
Speech Emotion Recognition Flask API
Adapted for current folder structure and model
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import random
import time

# Try to import ML libraries, but don't fail if they're not available
try:
    import numpy as np
    import librosa
    import soundfile as sf
    import io
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("ML libraries not available, using mock predictions")

# Optional: silence TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

try:
    from tensorflow.keras.models import load_model
    TENSORFLOW_AVAILABLE = True
except Exception:
    load_model = None
    TENSORFLOW_AVAILABLE = False

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_CANDIDATES = [
    os.path.join(BASE_DIR, "trained_model.h5"),
]

MODEL_PATH = next((p for p in MODEL_CANDIDATES if os.path.exists(p)), None)
model = load_model(MODEL_PATH) if (MODEL_PATH and load_model and TENSORFLOW_AVAILABLE) else None

# Configure your preprocessing to match training
TARGET_SAMPLE_RATE = 22050  # Match predict.py
N_MFCC = 40

# Emotion labels matching predict.py
CLASS_LABELS = [
    "Neutral", "Calm", "Happy", "Sad", "Angry", "Fearful", "Disgust", "Surprised"
]

# Emojis for emotions (using simple text to avoid Unicode issues)
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


def extract_feature(data, sr, mfcc=True, chroma=True, mel=True):
    """
    Extract features from audio files into numpy array
    Matches the feature extraction from predict.py
    """
    result = np.array([])
    if mfcc:                          
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sr, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
    if chroma:
        stft = np.abs(librosa.stft(data))
        chroma_feat = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T, axis=0)
        result = np.hstack((result, chroma_feat))
    if mel:                             
        mel_feat = np.mean(librosa.feature.melspectrogram(y=data, sr=sr).T, axis=0)
        result = np.hstack((result, mel_feat))
    return result


def load_audio_from_bytes(file_storage, target_sr=TARGET_SAMPLE_RATE):
    """Reads uploaded audio file into a mono float32 numpy array at target_sr."""
    file_bytes = file_storage.read()
    
    # Reset file pointer
    file_storage.seek(0)
    
    # Try multiple approaches for better format support
    data = None
    sr = None
    
    # Method 1: Try soundfile first (best format support)
    try:
        file_storage.seek(0)
        data, sr = sf.read(io.BytesIO(file_bytes), dtype='float32', always_2d=False)
        if data.ndim > 1:
            data = np.mean(data, axis=1)
        print(f"Loaded with soundfile: {data.shape}, {sr}Hz")
    except Exception as e:
        print(f"Soundfile failed: {e}")
        
        # Method 2: Try librosa with different parameters
        try:
            file_storage.seek(0)
            data, sr = librosa.load(io.BytesIO(file_bytes), sr=None, mono=True)
            print(f"Loaded with librosa: {data.shape}, {sr}Hz")
        except Exception as e2:
            print(f"Librosa failed: {e2}")
            
            # Method 3: Try with specific format hints
            try:
                file_storage.seek(0)
                # Try different format hints
                for fmt in ['WAV', 'MP3', 'M4A', 'WEBM', 'OGG', 'FLAC']:
                    try:
                        file_storage.seek(0)
                        data, sr = sf.read(io.BytesIO(file_bytes), format=fmt, dtype='float32', always_2d=False)
                        if data.ndim > 1:
                            data = np.mean(data, axis=1)
                        print(f"Loaded with soundfile format {fmt}: {data.shape}, {sr}Hz")
                        break
                    except:
                        continue
                
                if data is None:
                    # Method 4: Try librosa with different parameters
                    try:
                        file_storage.seek(0)
                        data, sr = librosa.load(io.BytesIO(file_bytes), sr=None, mono=True, offset=0.0, duration=None)
                        print(f"Loaded with librosa (no offset): {data.shape}, {sr}Hz")
                    except Exception as e4:
                        print(f"All methods failed: {e4}")
                        raise Exception(f"Could not load audio file. Supported formats: WAV, MP3, M4A, WEBM, OGG, FLAC. Error: {str(e4)}")
                        
            except Exception as format_error:
                print(f"Format-specific loading failed: {format_error}")
                raise Exception(f"Could not load audio with any method: {str(format_error)}")

    # Ensure we have valid audio data
    if len(data) == 0:
        raise Exception("Audio file appears to be empty or corrupted")
    
    # Normalize audio data
    data = librosa.util.normalize(data)
    
    # Resample if necessary
    if sr != target_sr:
        data = librosa.resample(y=data, orig_sr=sr, target_sr=target_sr)
    
    # Normalize audio
    data = librosa.util.normalize(data)
    
    return data.astype(np.float32)


def build_model_input(features):
    """
    Build input tensor matching the model's expected input shape
    Based on predict.py's approach: expand_dims twice for (1, features, 1)
    """
    if not ML_AVAILABLE:
        return None
    # Expand dimensions to match model input: (batch, features, channels)
    feature = np.expand_dims(features, axis=0)  # Add batch dimension
    feature = np.expand_dims(feature, axis=2)   # Add channel dimension
    return feature

def mock_prediction():
    """
    Generate mock prediction when ML libraries are not available
    """
    # Simulate processing time
    time.sleep(0.5)
    
    # Random emotion prediction
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
    
    return {
        "predicted_emotion": predicted_emotion,
        "emoji": EMOTION_EMOJIS[predicted_emotion],
        "confidence": confidence,
        "all_probabilities": emotion_probs,
        "raw_prediction": probabilities,
        "input_shape": [1, 180, 1],
        "audio_info": {
            "duration": round(random.uniform(2, 10), 2),
            "sample_rate": TARGET_SAMPLE_RATE,
            "channels": 1
        },
        "method": "mock_prediction"
    }


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": bool(model),
        "model_path": MODEL_PATH,
        "ml_available": ML_AVAILABLE,
        "tensorflow_available": TENSORFLOW_AVAILABLE,
        "input_shape": getattr(model, 'input_shape', None) if model is not None else None,
        "supported_emotions": CLASS_LABELS,
        "emotion_emojis": EMOTION_EMOJIS,
        "prediction_mode": "real" if (ML_AVAILABLE and model) else "mock"
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return jsonify({"error": "Missing 'audio' file in form-data"}), 400

    file = request.files['audio']
    
    # Validate file
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check file size (limit to 10MB)
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size > 10 * 1024 * 1024:  # 10MB
        return jsonify({"error": "File too large. Maximum size is 10MB"}), 400
    
    if file_size == 0:
        return jsonify({"error": "Empty file"}), 400

    try:
        # Check if we have ML libraries and model available
        if not ML_AVAILABLE or model is None:
            print("Using mock prediction - ML libraries or model not available")
            response = mock_prediction()
            return jsonify(response), 200
        
        # Real prediction with ML libraries
        audio = load_audio_from_bytes(file)
        
        # Validate audio length
        if len(audio) < TARGET_SAMPLE_RATE * 0.1:  # Less than 0.1 seconds
            return jsonify({"error": "Audio too short. Minimum length is 0.1 seconds"}), 400
        
        if len(audio) > TARGET_SAMPLE_RATE * 30:  # More than 30 seconds
            return jsonify({"error": "Audio too long. Maximum length is 30 seconds"}), 400
        
        # Extract features using the same method as predict.py
        features = extract_feature(audio, TARGET_SAMPLE_RATE, mfcc=True, chroma=True, mel=True)
        input_tensor = build_model_input(features)
        
        # Validate input tensor
        if np.any(np.isnan(input_tensor)) or np.any(np.isinf(input_tensor)):
            return jsonify({"error": "Invalid audio data detected"}), 400
        
        # Make prediction
        prediction = model.predict(input_tensor, verbose=0)
        predicted_class = np.argmax(prediction, axis=1)[0]
        predicted_emotion = CLASS_LABELS[predicted_class]
        confidence = float(np.max(prediction))
        
        # Get all probabilities
        probabilities = prediction[0].tolist()
        emotion_probs = {emotion: float(prob) for emotion, prob in zip(CLASS_LABELS, probabilities)}
        
        response = {
            "predicted_emotion": predicted_emotion,
            "emoji": EMOTION_EMOJIS[predicted_emotion],
            "confidence": confidence,
            "all_probabilities": emotion_probs,
            "raw_prediction": prediction.tolist(),
            "input_shape": getattr(model, 'input_shape', None),
            "audio_info": {
                "duration": len(audio) / TARGET_SAMPLE_RATE,
                "sample_rate": TARGET_SAMPLE_RATE,
                "channels": 1
            },
            "method": "real_prediction"
        }

        return jsonify(response), 200
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        # Fallback to mock prediction on error
        print("Falling back to mock prediction due to error")
        response = mock_prediction()
        return jsonify(response), 200


@app.route('/emotions', methods=['GET'])
def get_emotions():
    """Get list of supported emotions with emojis"""
    return jsonify({
        "emotions": CLASS_LABELS,
        "emojis": EMOTION_EMOJIS
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5001'))
    print(f"Starting Speech Emotion Recognition API on port {port}")
    print(f"ML libraries available: {ML_AVAILABLE}")
    print(f"TensorFlow available: {TENSORFLOW_AVAILABLE}")
    print(f"Model loaded: {bool(model)}")
    if model:
        print(f"Model path: {MODEL_PATH}")
        print(f"Input shape: {model.input_shape}")
    else:
        print("Using mock predictions (ML libraries or model not available)")
    print(f"Supported emotions: {CLASS_LABELS}")
    app.run(host='0.0.0.0', port=port, debug=True)
