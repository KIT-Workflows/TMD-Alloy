#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to initialize conda
initialize_conda() {
    if [[ -f "$1/etc/profile.d/conda.sh" ]]; then
        source "$1/etc/profile.d/conda.sh"
    else
        echo "Could not find conda.sh in $1"
        exit 1
    fi
}

# Initialize variables
CONDA_BASE=""
ENV_MANAGER=""

# Detect environment manager
if command_exists mamba; then
    ENV_MANAGER="mamba"
    CONDA_BASE=$(conda info --base)
    initialize_conda "$CONDA_BASE"
    echo "Mamba is installed."
elif command_exists conda; then
    ENV_MANAGER="conda"
    CONDA_BASE=$(conda info --base)
    initialize_conda "$CONDA_BASE"
    echo "Conda is installed."
else
    echo "No conda or mamba found. Installing Mambaforge..."
    # Download and install Mambaforge
    INSTALLER=~/mambaforge.sh
    wget -O "$INSTALLER" https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
    bash "$INSTALLER" -b -p ~/mambaforge
    export PATH=~/mambaforge/bin:$PATH
    CONDA_BASE=~/mambaforge
    initialize_conda "$CONDA_BASE"
    ENV_MANAGER="mamba"
    echo "Mambaforge installed successfully."
    # Clean up installer
    rm -f "$INSTALLER"
fi

# Ensure mamba is available if it's supposed to be
if ! command_exists mamba && [[ "$ENV_MANAGER" == "mamba" ]]; then
    echo "Mamba command not found after installation."
    exit 1
fi

# Check if 'playground_simstack' environment exists
if conda env list | grep -qE "^[^#]*playground_simstack\s"; then
    echo "Environment 'playground_simstack' already exists."
else
    echo "Creating environment 'playground_simstack'."
    $ENV_MANAGER create -n playground_simstack python=3.12 -y
fi

# Activate the environment
echo "Activating environment 'playground_simstack'."
conda activate playground_simstack

# Install packages from requirements.txt
if [[ -f requirements.txt ]]; then
    echo "Checking and installing packages from requirements.txt."
    while read -r package; do
        # Skip empty lines and comments
        if [[ -z "$package" ]] || [[ "$package" == \#* ]]; then
            continue
        fi
        # Extract package name without version specifier
        package_name=$(echo "$package" | sed 's/[<>=!].*//')
        # Check if package is installed
        if ! pip show "$package_name" >/dev/null 2>&1; then
            echo "Package '$package_name' is not installed. Installing..."
            pip install "$package"
        else
            echo "Package '$package_name' is already installed."
        fi
    done < requirements.txt
else
    echo "requirements.txt not found. No packages to install."
fi

echo "Script finished successfully."
