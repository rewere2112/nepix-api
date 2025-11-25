#!/bin/bash
# Start Nepix API Server

cd "$(dirname "$0")"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    ./venv/bin/pip install -r requirements.txt
else
    source venv/bin/activate
    # Ensure dependencies are up to date even if venv exists
    ./venv/bin/pip install -r requirements.txt
fi

# Start the server
echo "🚀 Starting Nepix API Server..."
./venv/bin/python app.py
