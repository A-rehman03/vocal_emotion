# JTalk Web Interface

A modern, responsive web interface for the JTalk AI chatbot with real-time conversation capabilities.

## Features

- 🎨 **Modern UI Design**: Beautiful, responsive interface with gradient backgrounds and smooth animations
- 💬 **Real-time Chat**: Instant message exchange with typing indicators
- 🤖 **AI Integration**: Seamless integration with the JTalk chatbot backend
- 📱 **Mobile Responsive**: Works perfectly on desktop, tablet, and mobile devices
- 🎯 **Smart Responses**: Uses both intent matching and transformer models for intelligent responses
- 📊 **Session Management**: Maintains conversation history per session
- 🔄 **Auto-refresh Status**: Real-time status monitoring of the chatbot system

## Quick Start

### Option 1: Windows Batch File (Recommended)
1. Double-click `start_web_chat.bat`
2. Wait for dependencies to install
3. Browser will open automatically to `http://localhost:5002`

### Option 2: Manual Python Execution
1. Open terminal/command prompt in the chatbot folder
2. Run: `python run_web_interface.py`
3. Open browser to `http://localhost:5002`

### Option 3: Direct Flask Server
1. Install requirements: `pip install flask flask-cors`
2. Run: `python web_server.py`
3. Open browser to `http://localhost:5002`

## Interface Overview

### Header
- **JTalk AI Assistant** title with version info
- **Status indicator** showing connection status
- **Real-time status updates**

### Chat Area
- **Welcome message** for new users
- **Message bubbles** with user/bot differentiation
- **Timestamps** for each message
- **Smooth animations** for new messages
- **Auto-scroll** to latest messages

### Input Area
- **Auto-resizing textarea** for multi-line messages
- **Send button** with hover effects
- **Action buttons** for clearing chat and checking status
- **Keyboard shortcuts** (Enter to send, Shift+Enter for new line)

## API Endpoints

### POST `/api/chat`
Send a message to the chatbot
```json
{
    "message": "Hello, how are you?",
    "session_id": "session_123456"
}
```

### GET `/api/status`
Check chatbot system status
```json
{
    "status": "running",
    "chatbot_initialized": true,
    "intents_loaded": true,
    "timestamp": "2024-12-18T10:30:00"
}
```

### POST `/api/clear`
Clear conversation history for a session
```json
{
    "session_id": "session_123456"
}
```

### GET `/api/intents`
Get available intent tags
```json
{
    "intents": ["greeting", "goodbye", "help", "question"]
}
```

## Configuration

### Port Configuration
The web server runs on port 5002 by default. To change this:
1. Set environment variable: `set PORT=8080`
2. Or modify `web_server.py` line: `port = int(os.environ.get('PORT', 5002))`

### Customization
- **Colors**: Modify CSS variables in `templates/chat.html`
- **Messages**: Edit welcome message and responses in the HTML
- **Features**: Add new API endpoints in `web_server.py`

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Run: `pip install flask flask-cors transformers torch numpy`

2. **Port already in use**
   - Change port in `web_server.py` or kill existing process
   - Windows: `netstat -ano | findstr :5002`

3. **Chatbot not responding**
   - Check if `chatbot3.py` is working
   - Verify `intents.json` exists and is valid
   - Check console for error messages

4. **Browser not opening**
   - Manually navigate to `http://localhost:5002`
   - Check firewall settings

### Debug Mode
To enable debug mode, change in `web_server.py`:
```python
app.run(host='0.0.0.0', port=port, debug=True)
```

## File Structure

```
chatbot/
├── web_server.py              # Flask web server
├── run_web_interface.py       # Launcher script
├── start_web_chat.bat         # Windows batch file
├── templates/
│   └── chat.html             # Main chat interface
├── chatbot3.py               # Chatbot backend
├── intents.json              # Intent definitions
└── WEB_INTERFACE_README.md   # This file
```

## Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- **Lightweight**: Minimal dependencies, fast loading
- **Responsive**: Smooth animations and interactions
- **Efficient**: Auto-scroll, message history management
- **Scalable**: Session-based conversation management

## Security Notes

- Session management for conversation history
- Input validation and sanitization
- CORS enabled for development
- Change secret key in production

## Contributing

To add new features:
1. Modify `web_server.py` for backend changes
2. Update `templates/chat.html` for UI changes
3. Test across different browsers
4. Update this README

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Check console logs for error messages
4. Ensure chatbot backend is working properly
