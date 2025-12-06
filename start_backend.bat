@echo off
echo Activating virtual environment and starting backend server...
call backend\venv\Scripts\activate.bat
cd backend
python main.py
pause

