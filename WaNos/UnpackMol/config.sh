#!/bin/bash


# Exit immediately if a command exits with a non-zero status
set -e

# Run the environment setup script
chmod +x env_check_and_setup.sh
# Source the script to run it in the current shell
source ./env_check_and_setup.sh

# Name of the environment
env_name="playground_simstack"

# Function to display error messages
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Check if conda is available
if ! command -v conda &>/dev/null; then
    error_exit "'conda' command not found. Please load or install Anaconda or Miniconda."
fi

# Get the environment list and extract the path
env_path=$(conda env list | grep -w "$env_name" | awk '{print $NF}') || true

# Check if the environment was found
if [ -z "$env_path" ]; then
    error_exit "Environment '$env_name' not found."
else
    echo "Environment '$env_name' is located at: $env_path"

    # Split the path into two variables at "envs/"
    part1="${env_path%envs/*}envs/"
    part2="${env_path##*envs/}"

    # Create a new variable by concatenating part1 and "etc/profile.d/conda.sh"
    conda_sh_path="${part1%envs/}etc/profile.d/conda.sh"

    # Check if the conda.sh script exists
    if [ ! -f "$conda_sh_path" ]; then
        error_exit "Conda setup script not found at: $conda_sh_path"
    fi
    echo "Conda setup script is located at: $conda_sh_path"
fi

# # Set the POTCAR_PATH environment variable
# export POTCAR_PATH="/shared/software/chem/vasp/potpaw_PBE.54/"

# Run the environment setup script if it exists
env_setup_script="env_check_and_setup.sh"
if [ -f "$env_setup_script" ]; then
    chmod +x "$env_setup_script"
    # Source the script to run it in the current shell
    source "./$env_setup_script"
else
    echo "Warning: Environment setup script '$env_setup_script' not found. Skipping."
fi

# Source the conda setup script and activate the environment
source "$conda_sh_path"
conda activate "$env_name"

# Function to run a Python script and check for errors
run_python_script() {
    local script_name="$1"
    if [ -f "$script_name" ]; then
        echo "Running Python script: $script_name"
        python "$script_name"
    else
        error_exit "Python script '$script_name' not found."
    fi
}

# Run Python scripts
python_scripts=(
    "add_metadata.py"
    "unpackmol.py"
)

for script in "${python_scripts[@]}"; do
    run_python_script "$script"
done