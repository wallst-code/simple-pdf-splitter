#!/bin/bash
# Simple PDF Splitter - Mac Launcher
# Save this as SimplePDFSplitter.command and make executable

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 is required but not installed.\n\nPlease install from python.org" buttons {"OK"} default button "OK" with icon stop'
    exit 1
fi

# Check if this is first run
if [ ! -f ".deps_installed" ]; then
    echo "First run setup - installing dependencies..."
    echo "This will take about 30 seconds..."
    python3 -m pip install --user -q flask werkzeug PyMuPDF python-dotenv Flask-Limiter Flask-Talisman markdown
    touch .deps_installed
fi

# Start the application
echo "Starting Simple PDF Splitter..."
echo "Opening browser to http://localhost:5000"
echo ""
echo "To stop: Press Ctrl+C or close this window"
echo ""

# Open browser after a short delay
(sleep 3 && open http://localhost:5000) &

# Run the app
python3 main.py