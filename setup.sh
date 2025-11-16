#!/bin/bash

# Bash script to set up the AI Psychologist application

echo "Setting up AI Psychologist..."
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Found Python: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env
if [ -f ".env.example" ]; then
    if [ ! -f ".env" ]; then
        echo "Creating .env file from example..."
        cp .env.example .env
        echo "Please edit .env file to add your OpenRouter API key"
    else
        echo ".env file already exists"
    fi
fi

echo ""
echo "Setup complete!"
echo "================"
echo "Next steps:"
echo "1. Edit .env file to add your OpenRouter API key"
echo "2. Run ./run.sh to start the application"