# Deployment Guide for Vocal Emotion AI Project

This guide provides instructions for deploying the three main components of your application:
1.  **Frontend**: React Application
2.  **Backend**: Node.js/Express Server
3.  **Emotion Service**: Python Flask API

---

## Prerequisites

-   GitHub account (to push your code)
-   Accounts on deployment platforms:
    -   **Vercel** (Recommended for Frontend)
    -   **Render** (Recommended for Backend & Python Service)
    -   *Alternative*: **Railway** or **Heroku**

---

## 1. Prepare Your Code for Deployment

### A. Push to GitHub
1.  Initialize a git repository in the root folder (`d:\vocal_emotion`) if you haven't already.
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a new repository on GitHub.
3.  Push your code to GitHub:
    ```bash
    git remote add origin <your-github-repo-url>
    git branch -M main
    git push -u origin main
    ```

### B. Environment Variables
Gather your keys from your local `.env` files. You will need to add these to the deployment platforms' "Environment Variables" settings.
-   **Backend**: `MONGO_URI`, `JWT_SECRET`, `PORT` (usually automated), `OPENAI_API_KEY`, etc.
-   **Frontend**: `REACT_APP_API_URL` (URL of your deployed Backend), `REACT_APP_EMOTION_SERVICE_URL` (URL of your deployed Emotion Service).

---

## 2. Deploy Backend (Node.js) to Render

1.  Log in to [Render](https://render.com/).
2.  Click **"New +"** -> **"Web Service"**.
3.  Connect your GitHub repository.
4.  Configure the service:
    -   **Name**: `vocal-emotion-backend`
    -   **Root Directory**: `backend` (Important! This tells Render where the Node app lives)
    -   **Environment**: Node
    -   **Build Command**: `npm install`
    -   **Start Command**: `node server.js`
5.  **Environment Variables**:
    -   Add `MONGO_URI`, `JWT_SECRET`, etc.
6.  Click **"Create Web Service"**.
7.  Wait for the build to finish. Copy the **Service URL** (e.g., `https://vocal-emotion-backend.onrender.com`).

---

## 3. Deploy Emotion Service (Python) to Render

Since the model files are large, the standard free tier on some platforms might struggle with timeouts or disk space if it tries to download them every time. However, since you have the model committed locally in `emotion_service/model`, it should work if your repo is not too large (GitHub has a 100MB file limit; if `model.safetensors` is >100MB, you verified it's tracked by LFS or ignored, but usually it's best to download at runtime or use Git LFS).
*Note: If your local model files are large and not in git, the code is already set up to fallback to downloading from HuggingFace.*

1.  On [Render](https://render.com/), click **"New +"** -> **"Web Service"**.
2.  Connect the **same** GitHub repository.
3.  Configure the service:
    -   **Name**: `vocal-emotion-python`
    -   **Root Directory**: `emotion_service`
    -   **Environment**: Python 3
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `gunicorn -w 1 -b 0.0.0.0:5002 app:app` (or `python app.py` if not using Gunicorn, but Gunicorn is production-standard. You may need to add `gunicorn` to `requirements.txt`).
        -   *Correction*: Since `gunicorn` isn't in your `requirements.txt`, adding it is recommended. For now, you can use `python app.py`.
        -   **Start Command (Simple)**: `python app.py`
4.  **Environment Variables**:
    -   Add any needed variables (e.g. `PORT` is usually 10000 on Render, so you might need to update `app.py` to use `os.environ.get("PORT", 5002)`).
5.  Click **"Create Web Service"**.
6.  Wait for deployment. Copy the **Service URL** (e.g., `https://vocal-emotion-python.onrender.com`).

**Important Update for Python App**:
Modify your `app.py` or the start command to listen on the port Render assigns (usually standard port 80 or provided via env var).
Change line 87 in `app.py` to:
```python
port = int(os.environ.get("PORT", 5002))
app.run(host="0.0.0.0", port=port)
```

---

## 4. Deploy Frontend (React) to Vercel

1.  Log in to [Vercel](https://vercel.com/).
2.  Click **"Add New..."** -> **"Project"**.
3.  Import your GitHub repository.
4.  Configure the project:
    -   **Framework Preset**: Create React App
    -   **Root Directory**: Edit this and select `frontend`.
5.  **Environment Variables**:
    -   `REACT_APP_API_URL`: The URL of your **Backend** from Step 2.
    -   `REACT_APP_EMOTION_SERVICE_URL`: The URL of your **Emotion Service** from Step 3.
    -   *(Check your frontend code to see exactly what variable names it uses for API endpoints)*.
6.  Click **"Deploy"**.
7.  Vercel will build and deploy your site. You will get a final public URL.

---

## 5. Manual Deployment (VPS - Ubuntu)

If you prefer a Virtual Private Server (e.g., AWS EC2, DigitalOcean Droplet):

1.  **Install Dependencies**:
    ```bash
    sudo apt update
    sudo apt install nodejs npm python3-pip python3-venv nginx git
    ```

2.  **Clone Repo**:
    ```bash
    git clone <your-repo-url>
    cd vocal_emotion
    ```

3.  **Run Backend (PM2)**:
    ```bash
    sudo npm install -g pm2
    cd backend
    npm install
    pm2 start server.js --name "backend"
    ```

4.  **Run Emotion Service**:
    ```bash
    cd ../emotion_service
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install gunicorn
    gunicorn -w 1 -b 0.0.0.0:5002 app:app --daemon
    ```

5.  **Frontend (Build & Serve with Nginx)**:
    -   Build the app:
        ```bash
        cd ../frontend
        npm install
        npm run build
        ```
    -   Configure Nginx to serve the `build` folder and proxy API requests.

---

## Troubleshooting

-   **CORS Errors**: If frontend fails to talk to backend, ensure your Backend `server.js` cors configuration allows the Vercel domain.
    ```javascript
    app.use(cors({ origin: "https://your-frontend.vercel.app" }));
    ```
-   **Model Loading**: If the Python service fails due to "OOM" (Out of Memory) or timeout, try upgrading the instance type or ensuring you aren't downloading 2GB+ files on every boot.
