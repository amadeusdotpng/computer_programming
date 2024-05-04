#!/bin/bash

# Get parent directory name
parent_directory_name=$(basename "$(dirname "$(pwd)")")

# Get current directory name stripped of the port
current_directory_name_stripped=$(basename "$(pwd)" | sed 's/_[0-9]*$//')

# Get the port number
port=$(basename "$(pwd)" | sed 's/.*_//')

# Get the exposed port from the Dockerfile
exposed_port=$(ggrep -oP 'EXPOSE \K[0-9]+' Dockerfile)
echo "port=$port"
echo "exposed_port=$exposed_port"

# Build the Docker image
docker_image_name="${parent_directory_name}_${current_directory_name_stripped}"
echo "docker_image_name=$docker_image_name"
docker stop "$docker_image_name" >/dev/null 2>&1 || true
docker rm "$docker_image_name" >/dev/null 2>&1 || true
docker build -t "$docker_image_name" .

# Run the Docker container
docker run -d -p "$port:$exposed_port" --name "$docker_image_name" "$docker_image_name"
