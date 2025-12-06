@echo off
echo Starting Tomato Disease Model Training...
echo.
cd /d "%~dp0"
call backend\venv\Scripts\activate.bat
python cnn_train_transfer_learning.py
pause

