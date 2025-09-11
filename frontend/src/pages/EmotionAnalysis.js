import React, { useRef, useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

export default function EmotionAnalysis() {
	const fileInputRef = useRef(null);
	const mediaRecorderRef = useRef(null);
	const [recording, setRecording] = useState(false);
	const [chunks, setChunks] = useState([]);
	const [result, setResult] = useState(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState('');

	const handleUpload = async (file) => {
		setError('');
		setLoading(true);
		setResult(null);
		try {
			const formData = new FormData();
			formData.append('audio', file);
			const res = await fetch(`${API_URL}/predict`, {
				method: 'POST',
				body: formData,
			});
			const data = await res.json();
			if (!res.ok) throw new Error(data.error || 'Prediction failed');
			setResult(data);
		} catch (e) {
			setError(e.message);
		} finally {
			setLoading(false);
		}
	};

	const onFileChange = (e) => {
		const file = e.target.files?.[0];
		if (file) handleUpload(file);
	};

	const startRecording = async () => {
		setError('');
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
			const mime = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') ? 'audio/webm;codecs=opus' : 'audio/webm';
			const mr = new MediaRecorder(stream, { mimeType: mime });
			setChunks([]);
			mr.ondataavailable = (e) => {
				if (e.data && e.data.size > 0) setChunks((prev) => [...prev, e.data]);
			};
			mr.onstop = async () => {
				const blob = new Blob(chunks, { type: mr.mimeType });
				const file = new File([blob], 'recording.webm', { type: mr.mimeType });
				handleUpload(file);
			};
			mediaRecorderRef.current = mr;
			mr.start();
			setRecording(true);
		} catch (e) {
			setError(e.message);
		}
	};

	const stopRecording = () => {
		const mr = mediaRecorderRef.current;
		if (mr && mr.state !== 'inactive') {
			mr.stop();
			setRecording(false);
		}
	};

	return (
		<div className="max-w-2xl mx-auto p-4">
			<h1 className="text-2xl font-bold mb-4">Emotion Analysis</h1>
			<div className="space-x-2 mb-4">
				<button
					className="px-4 py-2 bg-indigo-600 text-white rounded"
					onClick={() => fileInputRef.current?.click()}
				>
					Upload Audio
				</button>
				<input ref={fileInputRef} type="file" accept="audio/*" className="hidden" onChange={onFileChange} />

				{!recording ? (
					<button className="px-4 py-2 bg-green-600 text-white rounded" onClick={startRecording}>
						Start Recording
					</button>
				) : (
					<button className="px-4 py-2 bg-red-600 text-white rounded" onClick={stopRecording}>
						Stop Recording
					</button>
				)}
			</div>

			{loading && <div>Analyzing...</div>}
			{error && <div className="text-red-600">{error}</div>}
			{result && (
				<pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">{JSON.stringify(result, null, 2)}</pre>
			)}
		</div>
	);
}
