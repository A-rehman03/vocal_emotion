@echo off
echo Setting up JTalk AI Assistant...
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
echo.

echo Step 2: Starting JTalk API server...
echo The API server will run on http://localhost:5000
echo Keep this window open while using the React app.
echo.
python api_server.py
