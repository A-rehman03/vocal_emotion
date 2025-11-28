@echo off
echo Fixing DLL loading issue for JTalk Chatbot...
echo ================================================

cd /d "%~dp0"

echo Running DLL fix script...
python fix_dll_issue.py

pause
