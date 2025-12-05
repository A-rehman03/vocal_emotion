# Project Overview

## 1. Description
**Vocal Emotion AI** is a full-stack web application designed to analyze emotions from speech. It combines a modern interactive UI with a dedicated machine learning service for real-time audio analysis.

## 2. Technology Stack

### Frontend
-   **Language**: JavaScript (React)
-   **Framework**: React (Create React App)
-   **Styling**: Tailwind CSS
-   **State Management**: Zustand, React Query
-   **Key Libraries**: `framer-motion` (animations), `lucide-react` (icons), `wavesurfer.js` (audio viz)

### Backend
-   **Language**: JavaScript (Node.js)
-   **Framework**: Express.js
-   **Database**: MongoDB (via Mongoose)
-   **Authentication**: JWT (JSON Web Tokens)

### Emotion Service (Microservice)
-   **Language**: Python
-   **Framework**: Flask
-   **ML/AI**: PyTorch, Transformers (Hugging Face)
-   **Model**: `prithivMLmods/Speech-Emotion-Classification`

## 3. Project Structure

```text
vocal_emotion/
├── backend/                  # Node.js API Gateway & Auth
│   ├── models/               # MongoDB Schemas (User, etc.)
│   ├── routes/               # API Endpoints (Auth, etc.)
│   └── server.js             # Main server entry point
│
├── emotion_service/          # Python ML Service
│   ├── model/                # Local cache of ML model files
│   ├── samples/              # Audio test samples
│   ├── templates/            # HTML templates for service UI
│   └── app.py                # Flask application entry point
│
├── frontend/                 # React User Interface
│   ├── public/               # Static assets
│   └── src/
│       ├── components/       # Reusable UI components
│       ├── pages/            # Application pages (Home, Dashboard)
│       └── services/         # API integration logic
│
└── README.md                 # Run instructions
```
