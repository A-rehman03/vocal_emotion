# JTalk AI Assistant - React Integration

## 🚀 Quick Start

### 1. Start the JTalk API Server
```bash
# Navigate to chatbot directory
cd chatbot

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the API server
python api_server.py
```
The API will run on `http://localhost:5000`

### 2. Start the React Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start the React app
npm start
```
The React app will run on `http://localhost:3000`

## 🎯 Features

### **JTalk Integration**
- ✅ **Voice Input** - Click microphone to speak
- ✅ **AI Responses** - Powered by JTalk transformer model
- ✅ **Intent Learning** - Bot learns from conversations
- ✅ **Emotion Recognition** - Detects user emotions
- ✅ **Text-to-Speech** - Bot speaks responses aloud

### **API Endpoints**
- `POST /api/chat` - Send message to JTalk
- `POST /api/learn` - Teach JTalk new responses
- `GET /api/health` - Check API status

## 🔧 How It Works

1. **User speaks** into microphone
2. **Audio is recorded** and processed
3. **Text is sent** to JTalk API
4. **JTalk generates** AI response
5. **Response is spoken** back to user
6. **Emotion is detected** and displayed

## 🛠️ Troubleshooting

### API Server Issues
- Make sure Python dependencies are installed
- Check that port 5000 is available
- Verify JTalk chatbot files are in the same directory

### React App Issues
- Make sure API server is running first
- Check browser console for errors
- Verify microphone permissions are granted

### Voice Recognition Issues
- Ensure microphone is working
- Check browser permissions
- Try refreshing the page

## 📱 Usage

1. **Start Conversation** - Click the "Start Conversation" button
2. **Speak** - The app will automatically start listening
3. **Listen** - JTalk will respond with voice
4. **Continue** - The conversation continues automatically
5. **End** - Click "End Conversation" when done

## 🎨 Customization

- **API URL**: Change in `frontend/src/pages/Chat.js` line 90
- **Voice Settings**: Modify speech synthesis in the `speakText` function
- **UI Styling**: Update Tailwind classes in the Chat component
- **Emotion Detection**: Integrate with your emotion analysis backend

## 🔗 Architecture

```
React Frontend (Port 3000)
    ↓ HTTP Requests
JTalk API Server (Port 5000)
    ↓ Function Calls
Python Chatbot Core
    ↓ AI Processing
Transformers + Intent Matching
```

The integration maintains all original JTalk functionality while providing a modern React interface!
