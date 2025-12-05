# Vocal Emotion AI

This project is a comprehensive Vocal Emotion AI system consisting of a React frontend, a Node.js backend, and a Python-based Emotion Analysis service.

## Prerequisites

Before running the project, ensure you have the following installed:

-   **Node.js** (v14+ recommended)
-   **npm** (comes with Node.js)
-   **Python** (v3.8+ recommended)
-   **pip** (comes with Python)

## Installation and Running

The project is divided into three main components. You will need to run all three concurrently for the full application to function.

### 1. Backend (Node.js)

The backend handles user authentication and general API requests.

1.  Open a terminal and navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the server:
    ```bash
    npm run dev
    ```
    *The backend server will start on port `5000` (default).*

### 2. Emotion Analysis Service (Python)

This service uses a pre-trained model to analyze audio for emotions.

### 2. Emotion Analysis Service (Python)

This service uses a pre-trained model to analyze audio for emotions.

1.  Navigate to the `emotion_service` directory:
    ```bash
    cd emotion_service
    ```
2.  (Recommended) Use the provided start script which handles environment setup automatically:
    ```bash
    # Windows
    .\start_service.bat
    ```

    *Alternatively, you can set it up manually:*
    ```bash
    # Create and activate virtual environment (using Python 3.12 or compatible standard installation)
    py -3.12 -m venv venv
    .\venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt

    # Run the app
    python app.py
    ```
    *The analysis service will start on port `5002`.*

4.  Start the Flask application:
    ```bash
    python app.py
    ```
    *The analysis service will start on port `5002`.*

### 3. Frontend (React)

The frontend provides the user interface.

1.  Open a NEW terminal and navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the React application:
    ```bash
    npm start
    ```
    *The application will open in your browser at `http://localhost:3000`.*

## Project Structure

-   **`backend/`**: Node.js/Express server (Auth, DB connection).
-   **`frontend/`**: React application (UI, Vapi integration).
-   **`emotion_service/`**: Python/Flask service for ML-based audio emotion analysis.

## Troubleshooting

-   **Port Conflicts**: Ensure ports 3000, 5000, and 5002 are not currently in use.
-   **Dependency Errors**: If `npm install` fails, try deleting `node_modules` and `package-lock.json` and running `npm install` again.
-   **Python Path**: If `python` command is not found, try using `python3` or check your system's PATH variables.
-   **CORS Issues**: Ensure the backend allows requests from `http://localhost:3000`.
