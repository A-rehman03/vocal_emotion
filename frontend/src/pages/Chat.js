import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import { 
  Mic, 
  MicOff, 
  Bot, 
  User, 
  Volume2,
  VolumeX,
  Play,
  Pause,
  MessageCircle,
  Sparkles,
  Brain,
  Waves,
  Activity
} from 'lucide-react';
import LoadingSpinner from '../components/ui/LoadingSpinner';

const Chat = () => {
  const { user } = useAuth();
  const [isConversationActive, setIsConversationActive] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [conversationState, setConversationState] = useState('idle'); // idle, listening, processing, speaking
  const [currentEmotion, setCurrentEmotion] = useState(null);
  const [audioLevel, setAudioLevel] = useState(0);
  const [conversationCount, setConversationCount] = useState(0);
  const mediaRecorderRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const animationFrameRef = useRef(null);
  const speechSynthesisRef = useRef(null);
  const silenceTimeoutRef = useRef(null);
  const isConversationActiveRef = useRef(false);

  // Update ref when conversation state changes
  useEffect(() => {
    isConversationActiveRef.current = isConversationActive;
  }, [isConversationActive]);


  // Cleanup audio resources on component unmount
  useEffect(() => {
    return () => {
      // Clean up audio context
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
      
      // Cancel any pending animation frames
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      
      // Stop any ongoing speech synthesis
      if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
      }
      
      // Stop any ongoing recording
      if (mediaRecorderRef.current && isRecording) {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleVoiceMessage = async (audioBlob, transcription, emotion) => {
    console.log('Processing voice message...', { transcription, emotion });
    setConversationState('processing');
    setIsLoading(true);
    setConversationCount(prev => prev + 1);

    try {
      // Send audio to backend for emotion analysis and AI response
      const formData = new FormData();
      formData.append('audio', audioBlob, 'voice-message.wav');
      
      console.log('Sending audio to backend...');
      const response = await fetch('/api/emotion/analyze', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      const data = await response.json();
      console.log('Backend response:', data);
      
      if (data.analysis) {
        setCurrentEmotion(data.analysis.detectedEmotion);
        console.log('Speaking response:', data.response);
        
        // Speak the AI response
        await speakText(data.response);
      }
    } catch (error) {
      console.error('Voice processing error:', error);
      await speakText("I'm sorry, I had trouble processing your voice message. Could you please try again?");
    } finally {
      setIsLoading(false);
      setConversationState('idle');
    }
  };

  const speakText = async (text) => {
    console.log('Starting to speak:', text);
    if ('speechSynthesis' in window) {
      setConversationState('speaking');
      setIsSpeaking(true);
      
      return new Promise((resolve) => {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 0.8;
        
        utterance.onend = () => {
          console.log('Speech ended, starting to listen again...');
          setIsSpeaking(false);
          setConversationState('idle');
          // Auto-start listening after AI finishes speaking if conversation is still active
          setTimeout(() => {
            if (isConversationActiveRef.current && conversationState === 'idle' && !isRecording) {
              console.log('Auto-starting recording...');
              startRecording();
            }
          }, 1000); // 1 second delay before auto-starting
          resolve();
        };
        
        utterance.onerror = (error) => {
          console.error('Speech synthesis error:', error);
          setIsSpeaking(false);
          setConversationState('idle');
          resolve();
        };
        
        speechSynthesis.speak(utterance);
      });
    } else {
      console.log('Speech synthesis not supported');
    }
  };

  const startRecording = async () => {
    console.log('Starting recording...');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 16000
        } 
      });
      console.log('Microphone access granted');
      
      // Set up audio analysis for visual feedback
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      
      analyserRef.current.fftSize = 256;
      const bufferLength = analyserRef.current.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);
      
      const updateAudioLevel = () => {
        if (analyserRef.current && isRecording) {
          analyserRef.current.getByteFrequencyData(dataArray);
          const average = dataArray.reduce((a, b) => a + b) / bufferLength;
          const normalizedLevel = average / 255;
          setAudioLevel(normalizedLevel);
          
          // Voice activity detection - stop recording after 2 seconds of silence
          // But only if we've been recording for at least 2 seconds
          if (normalizedLevel < 0.02) { // Low audio level threshold
            if (!silenceTimeoutRef.current && recordingTime >= 2) {
              console.log('Silence detected, starting timeout...');
              silenceTimeoutRef.current = setTimeout(() => {
                if (isRecording && isConversationActiveRef.current) {
                  console.log('Auto-stopping recording due to silence');
                  stopRecording();
                }
              }, 2000); // 2 seconds of silence
            }
          } else {
            // Clear silence timeout if there's audio activity
            if (silenceTimeoutRef.current) {
              console.log('Audio activity detected, clearing silence timeout');
              clearTimeout(silenceTimeoutRef.current);
              silenceTimeoutRef.current = null;
            }
          }
          
          animationFrameRef.current = requestAnimationFrame(updateAudioLevel);
        }
      };
      
      const mr = new MediaRecorder(stream);
      mediaRecorderRef.current = mr;
      setRecordingTime(0);
      setIsRecording(true);
      setIsListening(true);
      setConversationState('listening');
      
      // Start the timer
      const timerInterval = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
      
      // Set minimum recording time
      const minRecordingTime = 2000; // 2 seconds minimum
      
      const audioChunks = [];
      
      mr.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunks.push(e.data);
        }
      };
      
      mr.onstop = async () => {
        console.log('Recording stopped, processing audio...');
        setIsRecording(false);
        setIsListening(false);
        setAudioLevel(0);
        
        // Clear the timer
        clearInterval(timerInterval);
        
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current);
        }
        
        // Clear silence timeout
        if (silenceTimeoutRef.current) {
          clearTimeout(silenceTimeoutRef.current);
          silenceTimeoutRef.current = null;
        }
        
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        console.log('Audio blob created, size:', audioBlob.size);
        
        // Simulate transcription and emotion detection
        // In a real implementation, you would send this to a speech-to-text service
        const mockTranscription = `Voice message (${formatTime(recordingTime)})`;
        const mockEmotion = ['happy', 'sad', 'angry', 'neutral', 'excited', 'calm'][Math.floor(Math.random() * 6)];
        
        await handleVoiceMessage(audioBlob, mockTranscription, mockEmotion);
        
        // Clean up
        stream.getTracks().forEach(track => track.stop());
        if (audioContextRef.current) {
          audioContextRef.current.close();
        }
      };
      
      mr.start();
      updateAudioLevel();
    } catch (error) {
      console.error('Recording failed:', error);
      setConversationState('idle');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
    }
  };

  const startConversation = async () => {
    setIsConversationActive(true);
    setConversationCount(0);
    setCurrentEmotion(null);
    // Start listening immediately
    await startRecording();
  };

  const endConversation = () => {
    setIsConversationActive(false);
    
    // Stop any ongoing recording
    if (isRecording) {
      stopRecording();
    }
    
    // Stop any ongoing speech
    if (isSpeaking) {
      speechSynthesis.cancel();
      setIsSpeaking(false);
    }
    
    // Clear any timeouts
    if (silenceTimeoutRef.current) {
      clearTimeout(silenceTimeoutRef.current);
    }
    
    // Reset states
    setConversationState('idle');
    setCurrentEmotion(null);
    setAudioLevel(0);
    setRecordingTime(0);
  };

  const toggleVoiceInput = () => {
    if (isRecording) {
      stopRecording();
    } else {
      // If AI is speaking, stop it and start listening
      if (isSpeaking) {
        speechSynthesis.cancel();
        setIsSpeaking(false);
        setConversationState('idle');
        setTimeout(() => startRecording(), 500);
      } else {
        startRecording();
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-primary-50/30 dark:from-dark-900 dark:via-dark-800 dark:to-dark-900 flex flex-col">
      {/* Header */}
      <motion.div 
        className="bg-white/80 dark:bg-dark-800/80 backdrop-blur-xl border-b border-white/20 dark:border-dark-700/50 px-6 py-6 shadow-xl"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="h-12 w-12 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center shadow-lg">
              <Brain className="h-7 w-7 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">AI Chat Assistant</h1>
              <p className="text-sm text-gray-600 dark:text-gray-300 font-medium">Powered by emotion recognition</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600 dark:text-gray-300 font-semibold">Online</span>
          </div>
        </div>
      </motion.div>

      {/* Conversation Area */}
      <div className="flex-1 flex items-center justify-center px-6 py-6">
        {!isConversationActive ? (
          <motion.div 
            className="flex flex-col items-center justify-center text-center"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
          >
            <div className="relative mb-8">
              <div className="w-32 h-32 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center shadow-2xl">
                <MessageCircle className="h-16 w-16 text-white" />
              </div>
              <div className="absolute -top-2 -right-2 w-10 h-10 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center animate-bounce shadow-lg">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
            </div>
            <h3 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Ready to Chat?
            </h3>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-lg leading-relaxed mb-8">
              Start a natural voice conversation with our AI assistant that understands emotions and responds with voice.
            </p>
            <motion.button
              onClick={startConversation}
              className="px-8 py-4 bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white text-lg font-semibold rounded-2xl shadow-2xl transition-all duration-300 hover:scale-105"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Start Conversation
            </motion.button>
          </motion.div>
        ) : (
          <motion.div 
            className="flex flex-col items-center justify-center text-center"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
          >
            {/* Main Conversation Icon */}
            <div className="relative mb-8">
              <motion.div 
                className={`w-32 h-32 rounded-full flex items-center justify-center shadow-2xl ${
                  conversationState === 'listening' ? 'bg-gradient-to-br from-red-500 to-red-600' :
                  conversationState === 'processing' ? 'bg-gradient-to-br from-yellow-500 to-orange-500' :
                  conversationState === 'speaking' ? 'bg-gradient-to-br from-green-500 to-emerald-500' :
                  'bg-gradient-to-br from-primary-500 to-secondary-500'
                }`}
                animate={{
                  scale: conversationState === 'listening' ? [1, 1.1, 1] : 1,
                }}
                transition={{
                  duration: 1,
                  repeat: conversationState === 'listening' ? Infinity : 0,
                  ease: "easeInOut"
                }}
              >
                {conversationState === 'listening' ? (
                  <Mic className="h-16 w-16 text-white" />
                ) : conversationState === 'processing' ? (
                  <Activity className="h-16 w-16 text-white animate-pulse" />
                ) : conversationState === 'speaking' ? (
                  <Volume2 className="h-16 w-16 text-white" />
                ) : (
                  <MessageCircle className="h-16 w-16 text-white" />
                )}
              </motion.div>
              
              {/* Audio Level Visualization */}
              {conversationState === 'listening' && (
                <div className="absolute inset-0 rounded-full border-4 border-red-300 animate-ping"></div>
              )}
              
              {/* Emotion Indicator */}
              {currentEmotion && (
                <div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 px-4 py-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white text-sm font-semibold rounded-full shadow-lg">
                  {currentEmotion}
                </div>
              )}
            </div>

            {/* Conversation Status */}
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              {conversationState === 'listening' ? 'Listening...' :
               conversationState === 'processing' ? 'Processing...' :
               conversationState === 'speaking' ? 'AI is speaking...' :
               'Conversation Active'}
            </h3>
            
            <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
              {conversationState === 'listening' ? `Speak now... (${formatTime(recordingTime)})` :
               conversationState === 'processing' ? 'Analyzing your voice...' :
               conversationState === 'speaking' ? 'AI is responding...' :
               'Ready to listen'}
            </p>

            {/* Conversation Stats */}
            <div className="flex items-center space-x-6 text-sm text-gray-500 dark:text-gray-400 mb-8">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-gradient-to-r from-green-500 to-accent-500 rounded-full"></div>
                <span className="font-semibold">Conversation #{conversationCount}</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"></div>
                <span className="font-semibold">Emotion Aware</span>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-4">
              {isRecording && (
                <motion.button
                  onClick={stopRecording}
                  className="px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-semibold rounded-xl shadow-lg transition-all duration-300 hover:scale-105"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Stop Recording
                </motion.button>
              )}
              
              <motion.button
                onClick={endConversation}
                className="px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-semibold rounded-xl shadow-lg transition-all duration-300 hover:scale-105"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                End Conversation
              </motion.button>
            </div>
          </motion.div>
        )}
      </div>

    </div>
  );
};

export default Chat;
