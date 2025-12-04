#!/bin/bash
# Contributor setup script for Mac/Linux
set -e

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

get_python_version() {
    "$1" --version 2>&1 | awk '{print $2}' | cut -d'.' -f1,2
}

version_ge() {
    printf '%s\n%s\n' "$2" "$1" | sort -V -C
}

install_python_mac() {
    echo "Installing Python 3.12 via Homebrew..."
    
    if ! command_exists brew; then
        echo "Homebrew not found. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install python@3.12
    echo "Python 3.12 installed successfully"
}

install_python_ubuntu() {
    echo "Installing Python 3.12..."
    sudo apt update
    sudo apt install -y python3.12 python3.12-venv python3.12-dev
    echo "Python 3.12 installed successfully"
}

install_python_fedora() {
    echo "Installing Python 3.12..."
    sudo dnf install -y python3.12 python3.12-devel
    echo "Python 3.12 installed successfully"
}

echo "Checking Python installation..."
PYTHON_CMD=""
REQUIRED_VERSION="3.12"

if command_exists python3.12; then
    PYTHON_VERSION=$(get_python_version python3.12)
    if version_ge "$PYTHON_VERSION" "$REQUIRED_VERSION"; then
        PYTHON_CMD="python3.12"
        echo "Found python3.12: $PYTHON_VERSION"
    fi
fi

if [ -z "$PYTHON_CMD" ] && command_exists python3; then
    PYTHON_VERSION=$(get_python_version python3)
    if version_ge "$PYTHON_VERSION" "$REQUIRED_VERSION"; then
        PYTHON_CMD="python3"
        echo "Found python3: $PYTHON_VERSION"
    fi
fi

if [ -z "$PYTHON_CMD" ] && command_exists python; then
    PYTHON_VERSION=$(get_python_version python)
    if version_ge "$PYTHON_VERSION" "$REQUIRED_VERSION"; then
        PYTHON_CMD="python"
        echo "Found python: $PYTHON_VERSION"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "Python 3.12 not found. Installing automatically..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        install_python_mac
        PYTHON_CMD="python3.12"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            case "$ID" in
                ubuntu|debian)
                    install_python_ubuntu
                    PYTHON_CMD="python3.12"
                    ;;
                fedora|rhel|centos)
                    install_python_fedora
                    PYTHON_CMD="python3.12"
                    ;;
                *)
                    echo "Unsupported Linux distribution: $ID"
                    echo "Please install Python 3.12 manually"
                    exit 1
                    ;;
            esac
        else
            echo "Cannot determine Linux distribution"
            echo "Please install Python 3.12 manually"
            exit 1
        fi
    else
        echo "Unsupported operating system: $OSTYPE"
        echo "Please install Python 3.12 manually"
        exit 1
    fi
    
    if ! command_exists $PYTHON_CMD; then
        echo "Python installation failed"
        exit 1
    fi
fi

echo "Setting up virtual environment..."

if [ -d "venv" ] && [ ! -f "venv/bin/activate" ]; then
    rm -rf venv
fi

if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
fi

source venv/bin/activate

VENV_PYTHON=$(which python)

echo "Installing dependencies..."
python -m pip install --upgrade pip --quiet

if [ ! -f "engine/requirements.txt" ]; then
    echo "requirements.txt not found in engine directory"
    exit 1
fi

pip install -r engine/requirements.txt --quiet

if [ ! -f "engine/requirements-dev.txt" ]; then
    echo "requirements-dev.txt not found in engine directory"
    exit 1
fi

pip install -r engine/requirements-dev.txt --quiet

echo "Setup completed successfully!"
