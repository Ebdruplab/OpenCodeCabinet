#!/bin/bash

echo "Creating virtual environment in .venv..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install nicegui pdf2image
source .venv/bin/activate
echo ""
echo "✅ Setup complete."
echo ""
echo "📦 NOTE: 'pdf2image' requires 'poppler' to be installed on your system."
echo "   macOS: brew install poppler"
echo "   Ubuntu: sudo apt install poppler-utils"
echo ""
echo "To activate the environment later:"
echo "source .venv/bin/activate"
echo "python main.py"
