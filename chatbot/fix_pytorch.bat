@echo off
echo Fixing PyTorch DLL loading issue...
echo ===================================

cd /d "%~dp0"

echo Running PyTorch setup fix...
python fix_pytorch_setup.py

pause
