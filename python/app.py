from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import librosa
import soundfile as sf
import io

# Optional: silence TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

try:
	from tensorflow.keras.models import load_model
except Exception:
	load_model = None

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_CANDIDATES = [
	os.path.join(BASE_DIR, "Trained_Models", "model0.5.h5"),
	os.path.join(BASE_DIR, "Trained_Models", "model0.h5"),
]

MODEL_PATH = next((p for p in MODEL_CANDIDATES if os.path.exists(p)), None)
model = load_model(MODEL_PATH) if (MODEL_PATH and load_model) else None

# Configure your preprocessing to match training
TARGET_SAMPLE_RATE = 16000
N_MFCC = 40

# Optional: set your class labels here if known, otherwise leave None
CLASS_LABELS = [
	"angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"
]


def load_audio_from_bytes(file_storage, target_sr=TARGET_SAMPLE_RATE):
	"""Reads uploaded audio file into a mono float32 numpy array at target_sr."""
	file_bytes = file_storage.read()
	try:
		data, sr = sf.read(io.BytesIO(file_bytes), dtype='float32', always_2d=False)
		if data.ndim > 1:
			data = np.mean(data, axis=1)
	except Exception:
		data, sr = librosa.load(io.BytesIO(file_bytes), sr=None, mono=True)

	if sr != target_sr:
		data = librosa.resample(y=data, orig_sr=sr, target_sr=target_sr)
	return data.astype(np.float32)


def compute_mfcc_features(audio, sr=TARGET_SAMPLE_RATE, n_mfcc=N_MFCC):
	"""Return both time-averaged vector and time-sequence MFCCs.
	- pooled: shape (n_mfcc,)
	- sequence: shape (time_steps, n_mfcc)
	"""
	mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)  # (n_mfcc, t)
	pooled = np.mean(mfcc, axis=1)  # (n_mfcc,)
	sequence = mfcc.T  # (t, n_mfcc)
	return pooled.astype(np.float32), sequence.astype(np.float32)


def pad_or_trim_sequence(seq, target_time, target_feat):
	"""Pad or trim a (time, feat) array to (target_time, target_feat)."""
	t, f = seq.shape
	# adjust features first
	if f < target_feat:
		pad_f = target_feat - f
		seq = np.pad(seq, ((0, 0), (0, pad_f)), mode='constant')
	elif f > target_feat:
		seq = seq[:, :target_feat]
	# adjust time dimension (center-crop/pad)
	if t < target_time:
		pad_t = target_time - t
		left = pad_t // 2
		right = pad_t - left
		seq = np.pad(seq, ((left, right), (0, 0)), mode='constant')
	elif t > target_time:
		start = (t - target_time) // 2
		seq = seq[start:start + target_time, :]
	return seq


def pad_or_trim_vector(vec, target_len):
	"""Pad or trim a 1D vector to target_len."""
	l = vec.shape[0]
	if l < target_len:
		pad = target_len - l
		vec = np.pad(vec, (0, pad), mode='constant')
	elif l > target_len:
		vec = vec[:target_len]
	return vec


def build_model_input(pooled_vec, seq_matrix, input_shape):
	"""Build an input tensor matching model.input_shape (including batch dim).
	input_shape is typically like (None, features) or (None, time, features[, channels]).
	"""
	# Remove batch dim (None)
	dims = list(input_shape[1:]) if isinstance(input_shape, (list, tuple)) else []
	if len(dims) == 1:
		# Vector model: (None, features)
		n_features = dims[0] if dims[0] is not None else pooled_vec.shape[0]
		vec = pad_or_trim_vector(pooled_vec, n_features)
		return vec.reshape(1, n_features)
	elif len(dims) >= 2:
		# Sequence model: (None, time, features[, channels])
		time_dim = dims[0] if dims[0] is not None else seq_matrix.shape[0]
		feat_dim = dims[1] if dims[1] is not None else seq_matrix.shape[1]
		seq = pad_or_trim_sequence(seq_matrix, time_dim, feat_dim)
		if len(dims) == 2:
			# (batch, time, features)
			return seq.reshape(1, time_dim, feat_dim)
		else:
			# Assume channels last: (batch, time, features, channels)
			channels = dims[2] if dims[2] is not None else 1
			seq = seq.reshape(1, time_dim, feat_dim)
			seq = np.expand_dims(seq, axis=-1)  # add channel dim
			if channels == 1:
				return seq
			# if channels>1, tile to match
			return np.tile(seq, (1, 1, 1, channels))
	# Fallback to vector
	n_features = pooled_vec.shape[0]
	return pooled_vec.reshape(1, n_features)


@app.route('/health', methods=['GET'])
def health():
	return jsonify({
		"status": "ok",
		"model_loaded": bool(model),
		"model_path": MODEL_PATH,
		"input_shape": getattr(model, 'input_shape', None) if model is not None else None,
	}), 200


@app.route('/predict', methods=['POST'])
def predict():
	if model is None:
		return jsonify({"error": "Model not loaded. Expected at: {}".format(MODEL_CANDIDATES)}), 500

	if 'audio' not in request.files:
		return jsonify({"error": "Missing 'audio' file in form-data"}), 400

	file = request.files['audio']
	try:
		audio = load_audio_from_bytes(file)
		pooled_vec, seq_matrix = compute_mfcc_features(audio)
		input_tensor = build_model_input(pooled_vec, seq_matrix, model.input_shape)
		pred = model.predict(input_tensor)
		pred = np.asarray(pred)

		response = {
			"raw": pred.tolist(),
			"argmax": int(np.argmax(pred)) if pred.ndim >= 2 and pred.shape[-1] else None,
			"input_shape": getattr(model, 'input_shape', None),
			"features": {
				"pooled_shape": list(pooled_vec.shape),
				"sequence_shape": list(seq_matrix.shape),
			},
		}

		# Optional label mapping if size matches
		if pred.ndim >= 2 and len(CLASS_LABELS) == pred.shape[-1]:
			probs = pred[0]
			pairs = sorted(zip(CLASS_LABELS, probs.tolist()), key=lambda x: x[1], reverse=True)
			response["labels"] = {
				"top1": pairs[0][0],
				"probs": {k: float(v) for k, v in pairs},
			}

		return jsonify(response), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
	port = int(os.environ.get('PORT', '5001'))
	app.run(host='0.0.0.0', port=port)
