#!/bin/bash

CODE_ARCHIVE=$1
ENV=$2

echo "Installing $CODE_ARCHIVE in environment $ENV"

# Function to extract package name from wheel file
extract_package_name() {
    local wheel_file=$1
    # Extract package name from wheel filename (before first hyphen)
    basename "$wheel_file" | cut -d'-' -f1
}

install_archive() {
    local venv_path=$1
    local service_name=$2

    if [[ -d /tmp/code_build ]]; then
        rm -rf /tmp/code_build/
    fi

    mkdir /tmp/code_build
    cd /tmp/code_build
    tar -xzf $CODE_ARCHIVE
    source /opt/code/build_venv/bin/activate
    python -m build --no-isolation --wheel

    deactivate
    local wheel_file=$(ls /tmp/code_build/dist/*.whl)

    # Extract package name from wheel file
    local package_name=$(extract_package_name "$wheel_file")
    echo "Package name: $package_name"

    # Activate virtual environment
    source "$venv_path/bin/activate"

    # Check if package is already installed and remove it
    if pip show "$package_name" > /dev/null 2>&1; then
        echo "Package $package_name is already installed, removing it first..."
        pip uninstall -y "$package_name"
    else
        echo "Package $package_name is not currently installed"
    fi

    # Install the wheel file
    pip install "$wheel_file"
    deactivate
    echo "Successfully installed $wheel_file in $venv_path"

    service $service_name restart
}

# Install based on environment
case "$ENV" in
    "prod")
        install_archive "/opt/beaker/venv" "beakerhub"
        ;;
    "beta")
        install_archive "/opt/beaker-beta/venv" "beakerhub-beta"
        ;;
    "all")
        install_archive "/opt/beaker/venv" "beakerhub"
        install_archive "/opt/beaker-beta/venv" "beakerhub-beta"
        ;;
    *)
        echo "Error: Invalid environment '$ENV'. Must be 'prod', 'beta', or 'all'"
        exit 1
        ;;
esac

echo "Deployment completed for environment: $ENV"
