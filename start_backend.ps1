# PowerShell script to start the backend server
Write-Host "Activating virtual environment and starting backend server..." -ForegroundColor Green
& ".\backend\venv\Scripts\Activate.ps1"
Set-Location backend
python main.py

