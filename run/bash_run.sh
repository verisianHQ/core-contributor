#!/bin/bash

# Change to parent directory
cd "$(dirname "$0")/.."

# Check if venv folder exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    bash setup/bash_setup.sh
    if [ $? -ne 0 ]; then
        echo "Setup failed. Exiting."
        exit 1
    fi
fi

# Check if python executable exists in venv
if [ ! -f "venv/bin/python3" ]; then
    echo "Python executable not found in virtual environment. Running setup..."
    bash setup/bash_setup.sh
    if [ $? -ne 0 ]; then
        echo "Setup failed. Exiting."
        exit 1
    fi
fi

# Activate venv and run test.py
source venv/bin/activate
echo "Running test.py..."
python3 test.py

deactivate
read -p "Press Enter to continue..."