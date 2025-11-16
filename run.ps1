# PowerShell script to run the AI Psychologist application

# Check if virtual environment exists
if (Test-Path ".\venv") {
    Write-Host "Activating virtual environment..."
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "No virtual environment found. Using system Python."
}

# Run the main application
Write-Host "Starting AI Psychologist..."
python src/main.py

Write-Host "Application finished."