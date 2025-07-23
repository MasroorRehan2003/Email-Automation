#!/bin/bash
# Activation script for Email Automation System

echo "🚀 Starting Email Automation System..."
echo "============================================"

# Activate virtual environment
source email_automation_env/bin/activate

# Check if we want to run a specific script
if [ "$1" = "quick" ]; then
    echo "Running Quick Start..."
    python quick_start.py
elif [ "$1" = "test" ]; then
    echo "Running System Tests..."
    python test_system.py
elif [ "$1" = "examples" ]; then
    echo "Running Examples..."
    python example_usage.py
elif [ "$1" = "advanced" ]; then
    echo "Running Advanced Features..."
    python advanced_automation.py
else
    echo "Available commands:"
    echo "  ./run.sh quick     - Quick start (send single email)"
    echo "  ./run.sh test      - Run system tests"
    echo "  ./run.sh examples  - Run example scripts"
    echo "  ./run.sh advanced  - Run advanced features"
    echo ""
    echo "Or run manually:"
    echo "  source email_automation_env/bin/activate"
    echo "  python email_automation.py"
fi
