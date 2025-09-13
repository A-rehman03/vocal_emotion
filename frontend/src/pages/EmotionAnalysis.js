import React, { useRef, useState, useEffect } from 'react';
import { 
  Mic, 
  MicOff, 
  Upload, 
  Brain, 
  AlertCircle, 
  CheckCircle, 
  Play,
  Pause,
  RotateCcw,
  Sparkles
} from 'lucide-react';
import ModernLoader from '../components/ui/ModernLoader';
import EmotionDisplay, { EmotionBreakdown } from '../components/ui/EmotionDisplay';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';


export default function EmotionAnalysis() {
  const fileInputRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioRef = useRef(null);
  const [recording, setRecording] = useState(false);
  const [chunks, setChunks] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [recordingTime, setRecordingTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);

  useEffect(() => {
    let interval;
    if (recording) {
      interval = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [recording]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleUpload = async (file) => {
    setError('');
    setLoading(true);
    setResult(null);
    setAudioUrl(URL.createObjectURL(file));
    
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
    setRecordingTime(0);
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
        setAudioUrl(URL.createObjectURL(blob));
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

  const togglePlayback = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const resetAnalysis = () => {
    setResult(null);
    setError('');
    setAudioUrl(null);
    setIsPlaying(false);
    setRecordingTime(0);
  };

  const getTopEmotion = () => {
    if (!result?.labels?.probs) return null;
    const emotions = Object.entries(result.labels.probs);
    return emotions.sort((a, b) => b[1] - a[1])[0];
  };

  const topEmotion = getTopEmotion();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-primary-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center space-x-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Brain className="h-4 w-4" />
            <span>AI-Powered Emotion Recognition</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Voice Emotion Analysis
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload an audio file or record your voice to discover the emotions hidden in your speech patterns
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="space-y-6">
            {/* Upload/Record Controls */}
            <div className="card">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                <Mic className="h-6 w-6 mr-2 text-primary-600" />
                Audio Input
              </h2>
              
              <div className="space-y-4">
                {/* File Upload */}
                <div className="relative">
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="w-full p-6 border-2 border-dashed border-gray-300 rounded-xl hover:border-primary-400 hover:bg-primary-50 transition-all duration-200 group"
                    disabled={loading || recording}
                  >
                    <div className="flex flex-col items-center space-y-3">
                      <Upload className="h-8 w-8 text-gray-400 group-hover:text-primary-600 transition-colors" />
                      <div className="text-center">
                        <p className="text-lg font-medium text-gray-700 group-hover:text-primary-700">
                          Upload Audio File
                        </p>
                        <p className="text-sm text-gray-500">
                          WAV, MP3, M4A, or WebM format
                        </p>
                      </div>
                    </div>
                  </button>
                  <input 
                    ref={fileInputRef} 
                    type="file" 
                    accept="audio/*" 
                    className="hidden" 
                    onChange={onFileChange}
                    disabled={loading || recording}
                  />
                </div>

                {/* Recording Controls */}
                <div className="flex items-center justify-center space-x-4">
                  <div className="text-center">
                    <p className="text-sm text-gray-500 mb-2">OR</p>
                  </div>
                </div>

                <div className="flex flex-col items-center space-y-4">
                  {!recording ? (
                    <button
                      onClick={startRecording}
                      disabled={loading}
                      className="btn-primary px-8 py-4 text-lg font-semibold flex items-center space-x-3 disabled:opacity-50 disabled:cursor-not-allowed group"
                    >
                      <Mic className="h-6 w-6 group-hover:scale-110 transition-transform" />
                      <span>Start Recording</span>
                    </button>
                  ) : (
                    <div className="flex flex-col items-center space-y-4">
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center space-x-2 bg-red-100 text-red-700 px-4 py-2 rounded-full">
                          <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                          <span className="font-mono text-lg">{formatTime(recordingTime)}</span>
                        </div>
                      </div>
                      <button
                        onClick={stopRecording}
                        className="btn-outline px-8 py-4 text-lg font-semibold flex items-center space-x-3 border-red-300 text-red-700 hover:bg-red-50"
                      >
                        <MicOff className="h-6 w-6" />
                        <span>Stop Recording</span>
                      </button>
                    </div>
                  )}
                </div>

                {/* Audio Playback */}
                {audioUrl && (
                  <div className="bg-gray-50 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-medium text-gray-700">Audio Preview</h3>
                      <button
                        onClick={togglePlayback}
                        className="p-2 rounded-lg bg-white hover:bg-gray-100 transition-colors"
                      >
                        {isPlaying ? (
                          <Pause className="h-5 w-5 text-gray-600" />
                        ) : (
                          <Play className="h-5 w-5 text-gray-600" />
                        )}
                      </button>
                    </div>
                    <audio
                      ref={audioRef}
                      src={audioUrl}
                      onEnded={() => setIsPlaying(false)}
                      className="w-full"
                    />
                  </div>
                )}
              </div>
            </div>

            {/* Loading State */}
            {loading && (
              <div className="card text-center animate-fade-in-up">
                <ModernLoader 
                  size="xl" 
                  text="Analyzing Audio" 
                  showBrain={true}
                  variant="brain"
                />
                <div className="mt-4">
                  <p className="text-gray-600">Our AI is processing your voice to detect emotions...</p>
                  <div className="mt-3 flex justify-center">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Error State */}
            {error && (
              <div className="card border-red-200 bg-red-50">
                <div className="flex items-start space-x-3">
                  <AlertCircle className="h-6 w-6 text-red-600 mt-0.5" />
                  <div>
                    <h3 className="font-semibold text-red-800 mb-1">Analysis Failed</h3>
                    <p className="text-red-700">{error}</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {result && (
              <>
                {/* Main Result */}
                <div className="card animate-fade-in-up">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                    <CheckCircle className="h-6 w-6 mr-2 text-green-600" />
                    Analysis Results
                  </h2>

                  {topEmotion && (
                    <div className="text-center mb-8">
                      <EmotionDisplay 
                        emotion={topEmotion[0]}
                        confidence={topEmotion[1]}
                        size="xl"
                        animated={true}
                        className="animate-scale-in"
                      />
                    </div>
                  )}

                  {/* Emotion Breakdown */}
                  {result.labels?.probs && (
                    <EmotionBreakdown 
                      emotions={result.labels.probs}
                      className="animate-slide-in-right"
                    />
                  )}
                </div>

                {/* Technical Details */}
                <div className="card animate-slide-in-left">
                  <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                    <Brain className="h-5 w-5 mr-2 text-primary-600" />
                    Technical Details
                  </h3>
                  <div className="space-y-3 text-sm">
                    <div className="flex justify-between items-center py-2 px-3 bg-gray-50 rounded-lg">
                      <span className="text-gray-600">Model Input Shape:</span>
                      <span className="font-mono text-gray-900 bg-white px-2 py-1 rounded border">
                        {result.input_shape?.join(' × ') || 'N/A'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 px-3 bg-gray-50 rounded-lg">
                      <span className="text-gray-600">Feature Shape:</span>
                      <span className="font-mono text-gray-900 bg-white px-2 py-1 rounded border">
                        {result.features?.sequence_shape?.join(' × ') || 'N/A'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 px-3 bg-gray-50 rounded-lg">
                      <span className="text-gray-600">Processing Time:</span>
                      <span className="font-mono text-gray-900 bg-white px-2 py-1 rounded border">
                        &lt; 1s
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 px-3 bg-gray-50 rounded-lg">
                      <span className="text-gray-600">Model Status:</span>
                      <span className="flex items-center text-green-600">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                        Active
                      </span>
                    </div>
                  </div>
                </div>

                {/* Reset Button */}
                <div className="flex justify-center animate-fade-in-up">
                  <button
                    onClick={resetAnalysis}
                    className="btn-outline px-8 py-4 flex items-center space-x-3 hover-lift group"
                  >
                    <RotateCcw className="h-5 w-5 group-hover:rotate-180 transition-transform duration-300" />
                    <span className="font-semibold">Analyze Another Audio</span>
                  </button>
                </div>
              </>
            )}

            {/* Empty State */}
            {!result && !loading && !error && (
              <div className="card text-center py-12 animate-fade-in-up">
                <div className="flex flex-col items-center space-y-6">
                  <div className="relative">
                    <div className="w-20 h-20 bg-gradient-to-br from-primary-100 to-primary-200 rounded-full flex items-center justify-center animate-float">
                      <Brain className="h-10 w-10 text-primary-600" />
                    </div>
                    <div className="absolute -top-2 -right-2 w-6 h-6 bg-yellow-400 rounded-full flex items-center justify-center animate-bounce">
                      <Sparkles className="h-3 w-3 text-yellow-800" />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">Ready to Analyze</h3>
                    <p className="text-gray-600 max-w-md mx-auto">
                      Upload an audio file or start recording to discover the emotions hidden in your voice
                    </p>
                  </div>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                      <span>AI-Powered</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                      <span>Real-time</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                      <span>Accurate</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
