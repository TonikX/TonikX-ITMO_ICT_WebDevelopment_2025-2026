#!/bin/bash

# Script to clean up Docker containers and free port 8000

echo "Cleaning up Docker containers..."

# Stop and remove containers
docker compose down 2>/dev/null || docker-compose down 2>/dev/null || true

# Remove old containers
docker ps -a --filter "name=hotel" --format "{{.ID}}" | xargs -r docker rm -f 2>/dev/null || true

# Kill any process on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Kill any process on port 8001
lsof -ti:8001 | xargs kill -9 2>/dev/null || true

echo "Cleanup complete!"
echo "You can now run: docker compose up --build"
