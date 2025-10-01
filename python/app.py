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


def compute_mfcc_features(audio, sr=TARGET_SAMPLE_RATE, n_mfcc=N_MFCC):
	"""Return both time-averaged vector and time-sequence MFCCs with improved preprocessing.
	- pooled: shape (n_mfcc,)
	- sequence: shape (time_steps, n_mfcc)
	"""
	# Remove silence from the beginning and end
	audio_trimmed, _ = librosa.effects.trim(audio, top_db=20)
	
	# If audio is too short, pad it
	if len(audio_trimmed) < sr * 0.5:  # Less than 0.5 seconds
		audio_trimmed = np.pad(audio_trimmed, (0, max(0, sr * 0.5 - len(audio_trimmed))), mode='constant')
	
	# Compute MFCC with additional features
	mfcc = librosa.feature.mfcc(y=audio_trimmed, sr=sr, n_mfcc=n_mfcc, n_fft=2048, hop_length=512)
	
	# Add delta features for better emotion recognition
	delta_mfcc = librosa.feature.delta(mfcc)
	delta2_mfcc = librosa.feature.delta(mfcc, order=2)
	
	# Combine MFCC with delta features
	combined_features = np.vstack([mfcc, delta_mfcc, delta2_mfcc])
	
	# Take only the first n_mfcc features to match expected input size
	combined_features = combined_features[:n_mfcc]
	
	pooled = np.mean(combined_features, axis=1)  # (n_mfcc,)
	sequence = combined_features.T  # (t, n_mfcc)
	
	# Normalize features
	pooled = (pooled - np.mean(pooled)) / (np.std(pooled) + 1e-8)
	sequence = (sequence - np.mean(sequence)) / (np.std(sequence) + 1e-8)
	
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
		audio = load_audio_from_bytes(file)
		
		# Validate audio length
		if len(audio) < TARGET_SAMPLE_RATE * 0.1:  # Less than 0.1 seconds
			return jsonify({"error": "Audio too short. Minimum length is 0.1 seconds"}), 400
		
		if len(audio) > TARGET_SAMPLE_RATE * 30:  # More than 30 seconds
			return jsonify({"error": "Audio too long. Maximum length is 30 seconds"}), 400
		
		pooled_vec, seq_matrix = compute_mfcc_features(audio)
		input_tensor = build_model_input(pooled_vec, seq_matrix, model.input_shape)
		
		# Validate input tensor
		if np.any(np.isnan(input_tensor)) or np.any(np.isinf(input_tensor)):
			return jsonify({"error": "Invalid audio data detected"}), 400
		
		pred = model.predict(input_tensor, verbose=0)
		pred = np.asarray(pred)
		
		# Validate prediction
		if np.any(np.isnan(pred)) or np.any(np.isinf(pred)):
			return jsonify({"error": "Model prediction failed"}), 500

		response = {
			"raw": pred.tolist(),
			"argmax": int(np.argmax(pred)) if pred.ndim >= 2 and pred.shape[-1] else None,
			"input_shape": getattr(model, 'input_shape', None),
			"features": {
				"pooled_shape": list(pooled_vec.shape),
				"sequence_shape": list(seq_matrix.shape),
			},
			"audio_info": {
				"duration": len(audio) / TARGET_SAMPLE_RATE,
				"sample_rate": TARGET_SAMPLE_RATE,
				"channels": 1
			}
		}

		# Optional label mapping if size matches
		if pred.ndim >= 2 and len(CLASS_LABELS) == pred.shape[-1]:
			probs = pred[0]
			
			# Apply confidence threshold
			max_prob = np.max(probs)
			if max_prob < 0.3:  # Low confidence threshold
				response["labels"] = {
					"top1": "uncertain",
					"confidence": float(max_prob),
					"probs": {k: float(v) for k, v in zip(CLASS_LABELS, probs.tolist())},
					"note": "Low confidence prediction"
				}
			else:
				pairs = sorted(zip(CLASS_LABELS, probs.tolist()), key=lambda x: x[1], reverse=True)
				response["labels"] = {
					"top1": pairs[0][0],
					"confidence": float(pairs[0][1]),
					"probs": {k: float(v) for k, v in pairs},
				}

		return jsonify(response), 200
	except Exception as e:
		print(f"Prediction error: {str(e)}")
		return jsonify({"error": f"Audio processing failed: {str(e)}"}), 500


if __name__ == '__main__':
	port = int(os.environ.get('PORT', '5001'))
	app.run(host='0.0.0.0', port=port)
