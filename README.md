# Vocal Emotion AI 🎤🧠

A cutting-edge AI-driven chatbot integrated with speech emotion recognition, designed to enhance human-computer interaction by providing emotionally aware responses. The system detects users' emotions from their speech and generates appropriate replies, improving user engagement and making interactions more natural.

## 🌟 Features

### Core Functionality
- **Speech Emotion Recognition**: Advanced AI models that analyze vocal patterns, tone, and voice characteristics
- **Emotion-Aware Chatbot**: Intelligent responses that adapt to detected emotional states
- **Real-Time Processing**: Instant emotion detection with minimal latency
- **Multi-Emotion Support**: Detects 8+ emotions including happy, sad, angry, neutral, excited, calm, anxious, and confident

### Technical Features
- **MERN Stack Architecture**: MongoDB, Express.js, React.js, Node.js
- **Complete Authentication System**: JWT-based authentication with user management
- **Responsive Design**: Modern, mobile-first UI built with Tailwind CSS
- **Real-Time Communication**: WebSocket support for live interactions
- **File Upload Support**: Audio file processing for emotion analysis
- **RESTful API**: Well-structured backend API with comprehensive endpoints

### User Experience
- **Beautiful Landing Page**: Modern design with compelling call-to-action
- **Dashboard Analytics**: User activity and emotion history tracking
- **Profile Management**: User preferences and settings customization
- **Responsive Navigation**: Intuitive navigation across all devices

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- MongoDB (v5 or higher)
- npm or yarn package manager

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment Configuration**
   Create a `.env` file in the backend directory:
   ```env
   PORT=5000
   NODE_ENV=development
   MONGODB_URI=mongodb://localhost:27017/vocal_emotion_ai
   JWT_SECRET=your_jwt_secret_key_here_make_it_long_and_secure
   JWT_EXPIRE=7d
   FRONTEND_URL=http://localhost:3000
   OPENAI_API_KEY=your_openai_api_key_here
   MAX_FILE_SIZE=10485760
   ```

4. **Start the server**
   ```bash
   npm run dev
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

## 🏗️ Project Structure

```
vocal_emotion/
├── backend/                 # Node.js backend server
│   ├── models/             # MongoDB schemas
│   ├── routes/             # API endpoints
│   ├── middleware/         # Authentication & validation
│   ├── server.js           # Main server file
│   └── package.json        # Backend dependencies
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   ├── App.js          # Main app component
│   │   └── index.js        # Entry point
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
└── README.md               # Project documentation
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user profile
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh JWT token

### User Management
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile
- `PUT /api/user/preferences` - Update user preferences
- `PUT /api/user/change-password` - Change password

### Emotion Analysis
- `POST /api/emotion/analyze` - Analyze audio file for emotions
- `POST /api/emotion/realtime` - Real-time emotion analysis
- `GET /api/emotion/history` - Get emotion analysis history
- `POST /api/emotion/feedback` - Submit feedback on analysis

### Chat
- `POST /api/chat/message` - Send text message to AI
- `POST /api/chat/voice` - Send voice message to AI
- `GET /api/chat/history` - Get chat conversation history
- `DELETE /api/chat/conversation/:id` - Delete conversation

## 🎨 UI Components

### Core Components
- **LoadingSpinner**: Reusable loading indicator with multiple sizes
- **Navbar**: Responsive navigation with authentication state
- **Footer**: Comprehensive footer with links and company info

### Pages
- **Home**: Landing page with features and call-to-action
- **Login**: User authentication form
- **Register**: User registration form
- **Dashboard**: User dashboard (protected route)
- **Chat**: AI chatbot interface (protected route)
- **EmotionAnalysis**: Voice emotion analysis (protected route)
- **Profile**: User profile management (protected route)

## 🔐 Authentication & Security

- **JWT Tokens**: Secure authentication with JSON Web Tokens
- **Password Hashing**: Bcrypt-based password security
- **Input Validation**: Comprehensive form validation using express-validator
- **Rate Limiting**: API rate limiting to prevent abuse
- **CORS Protection**: Cross-origin resource sharing configuration
- **Helmet Security**: Security headers and middleware

## 🎯 Future Enhancements

### Planned Features
- **Multilingual Support**: Support for multiple languages
- **Advanced AI Models**: Integration with state-of-the-art emotion recognition models
- **Voice Synthesis**: Text-to-speech with emotional intonation
- **Mobile App**: Native mobile applications for iOS and Android
- **Analytics Dashboard**: Advanced user analytics and insights
- **API Marketplace**: Public API for third-party integrations

### Technical Improvements
- **Microservices Architecture**: Scalable service-based architecture
- **Real-Time Streaming**: WebRTC for live audio streaming
- **Machine Learning Pipeline**: Automated model training and updates
- **Cloud Deployment**: AWS/Google Cloud deployment with auto-scaling

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI**: For inspiration and AI technology
- **Tailwind CSS**: For the beautiful UI framework
- **React Community**: For the amazing frontend ecosystem
- **Node.js Community**: For the robust backend platform

## 📞 Support

- **Email**: contact@vocalemotionai.com
- **Documentation**: [docs.vocalemotionai.com](https://docs.vocalemotionai.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/vocal-emotion-ai/issues)

## 🚀 Deployment

### Backend Deployment
```bash
# Production build
npm run build

# Start production server
npm start
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Deploy build folder to your hosting service
```

---

**Made with ❤️ and AI by the Vocal Emotion AI Team**

*Revolutionizing human-computer interaction through emotional intelligence*
