#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if Docker is installed
if ! command_exists docker; then
    echo "Docker is not installed. Installing Docker..."
    
    # Detect OS
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    else
        OS=$(uname -s)
    fi
    
    # Install Docker based on OS
    case $OS in
        ubuntu|debian|linuxmint)
            # Update package index
            sudo apt-get update
            # Install dependencies
            sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
            # Add Docker's official GPG key
            curl -fsSL https://download.docker.com/linux/$OS/gpg | sudo apt-key add -
            # Set up the stable repository
            sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$OS $(lsb_release -cs) stable"
            # Update package index again
            sudo apt-get update
            # Install Docker
            sudo apt-get install -y docker-ce docker-ce-cli containerd.io
            # Add current user to docker group
            sudo usermod -aG docker $USER
            echo "Docker installed successfully. You may need to log out and back in for group changes to take effect."
            ;;
        fedora|centos|rhel)
            # Install dependencies
            sudo yum install -y yum-utils device-mapper-persistent-data lvm2
            # Add Docker repository
            sudo yum-config-manager --add-repo https://download.docker.com/linux/$OS/docker-ce.repo
            # Install Docker
            sudo yum install -y docker-ce docker-ce-cli containerd.io
            # Start Docker
            sudo systemctl start docker
            # Enable Docker to start on boot
            sudo systemctl enable docker
            # Add current user to docker group
            sudo usermod -aG docker $USER
            echo "Docker installed successfully. You may need to log out and back in for group changes to take effect."
            ;;
        darwin)
            echo "macOS detected. Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
            exit 1
            ;;
        *)
            echo "Unsupported operating system. Please install Docker manually: https://docs.docker.com/get-docker/"
            exit 1
            ;;
    esac
    
    # Verify Docker installation
    if ! command_exists docker; then
        echo "Docker installation failed. Please install Docker manually: https://docs.docker.com/get-docker/"
        exit 1
    fi
else
    echo "Docker is already installed."
fi

# Check if Docker service is running
if ! docker info &> /dev/null; then
    echo "Starting Docker service..."
    if command_exists systemctl; then
        sudo systemctl start docker
    elif command_exists service; then
        sudo service docker start
    else
        echo "Could not start Docker service. Please start it manually."
        exit 1
    fi
fi

# Pull the latest image
echo "Pulling the latest image..."
docker pull ashansubodha1/200623p-lyrics-classify:latest

# Run the container
echo "Starting the container..."
docker run -d -p 80:8501 ashansubodha1/200623p-lyrics-classify:latest

# Wait a little for the app to start
echo "Waiting for the application to start..."
sleep 2

sudo ufw allow 80/tcp
sudo ufw enable
