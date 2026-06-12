#!/usr/bin/env bash
set -e

echo "Installing Aider+..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Install the aider package
echo "Installing python package..."
python3 -m pip install -e .

# Copy templates to ~/.aider-plus if they don't exist
AIDER_PLUS_DIR="$HOME/.aider-plus"

if [ ! -d "$AIDER_PLUS_DIR" ]; then
    echo "Initializing Aider+ configurations in $AIDER_PLUS_DIR..."
    cp -r aider-plus-templates "$AIDER_PLUS_DIR"
else
    echo "Found existing Aider+ configuration at $AIDER_PLUS_DIR."
    echo "Skipping template copy. If you want to reset, delete ~/.aider-plus and run this script again."
fi

echo "====================================="
echo "Aider+ installation complete!"
echo ""
echo "To start Aider+, use:"
echo "python3 -m aider"
echo ""
echo "Make sure to set your API keys either in your environment variables or in ~/.aider.conf.yml"
echo "Example:"
echo "export OPENAI_API_BASE=https://api.aicredits.in/v1"
echo "export OPENAI_API_KEY=your_key_here"
echo "====================================="
