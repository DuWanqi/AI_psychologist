# PowerShell script to set up the AI Psychologist application

Write-Host "Setting up AI Psychologist..."
Write-Host "=============================="

# Check if Python is installed
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Found Python: $pythonVersion"
} catch {
    Write-Host "Python not found. Please install Python 3.8 or higher."
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env
if (Test-Path ".env.example") {
    if (-not (Test-Path ".env")) {
        Write-Host "Creating .env file from example..."
        Copy-Item ".env.example" ".env"
        Write-Host "Please edit .env file to add your OpenRouter API key"
    } else {
        Write-Host ".env file already exists"
    }
}

Write-Host ""
Write-Host "Setup complete!"
Write-Host "================"
Write-Host "Next steps:"
Write-Host "1. Edit .env file to add your OpenRouter API key"
Write-Host "2. Run .\run.ps1 to start the application"