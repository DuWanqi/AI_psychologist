#!/bin/bash

# Bash script to run the AI Psychologist application

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "No virtual environment found. Using system Python."
fi

# Run the main application
echo "Starting AI Psychologist..."
python src/main.py

echo "Application finished."