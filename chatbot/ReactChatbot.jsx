import React, { useState, useRef, useEffect } from 'react';

const ReactChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  const API_BASE_URL = 'http://localhost:5000/api';

  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputMessage(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }

    // Add welcome message
    setMessages([{
      id: 1,
      text: "Hello! I am JTalk. How can I help you today?",
      sender: 'bot'
    }]);

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: message,
      sender: 'user'
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      if (data.status === 'success') {
        // Add bot response
        const botMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'bot'
        };
        setMessages(prev => [...prev, botMessage]);
        
        // Speak the response
        speakText(data.response);
      } else {
        console.error('API Error:', data.error);
        const errorMessage = {
          id: Date.now() + 1,
          text: 'Sorry, I encountered an error. Please try again.',
          sender: 'bot'
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Network Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I cannot connect to the server. Please make sure the API is running.',
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      setIsSpeaking(true);
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      speechSynthesis.speak(utterance);
    }
  };

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(inputMessage);
  };

  const learnIntent = async (userText, botResponse) => {
    try {
      const response = await fetch(`${API_BASE_URL}/learn`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: userText,
          response: botResponse
        }),
      });

      const data = await response.json();
      if (data.status === 'success') {
        console.log('Intent learned successfully');
      }
    } catch (error) {
      console.error('Failed to learn intent:', error);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h3>JTalk - AI Voice Assistant</h3>
        <div className="status-indicators">
          {isListening && <span className="status listening">🎤 Listening...</span>}
          {isSpeaking && <span className="status speaking">🔊 Speaking...</span>}
          {isLoading && <span className="status loading">⏳ Thinking...</span>}
        </div>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender}`}
          >
            <div className="message-content">
              {message.text}
            </div>
            {message.sender === 'bot' && (
              <button
                className="learn-button"
                onClick={() => learnIntent(messages[messages.length - 2]?.text, message.text)}
                title="Learn this response"
              >
                📚
              </button>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message or use voice..."
            className="message-input"
            disabled={isLoading}
          />
          <div className="button-group">
            <button
              type="button"
              onClick={isListening ? stopListening : startListening}
              className={`voice-button ${isListening ? 'listening' : ''}`}
              disabled={isLoading}
            >
              {isListening ? '🛑' : '🎤'}
            </button>
            <button
              type="submit"
              disabled={!inputMessage.trim() || isLoading}
              className="send-button"
            >
              Send
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default ReactChatbot;
