# PowerShell script to start training
Write-Host "Starting Tomato Disease Model Training..." -ForegroundColor Green
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Activate virtual environment
& ".\backend\venv\Scripts\Activate.ps1"

# Run training
Write-Host "Launching training script..." -ForegroundColor Yellow
python cnn_train_transfer_learning.py

Write-Host ""
Write-Host "Training completed or stopped." -ForegroundColor Green

