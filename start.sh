#!/bin/bash

# start.sh - Script to run both CLIProxyAPI (Go) and Hajimi (Python) in the same container
echo "Testing Nginx configuration..."
nginx -t 2>&1
echo "Starting Nginx multiplexer..."
nginx 2>&1 || echo "ERROR: Nginx failed to start!"


echo "Starting CLIProxyAPI in the background..."
# Ensure persistent config directory exists on the mounted volume
mkdir -p /app/data/cli-config
if [ ! -f /app/data/cli-config/config.yaml ]; then
    echo "Initializing default CLI config in persistent storage..."
    cp /CLIProxyAPI/config.yaml /app/data/cli-config/config.yaml
fi

cd /CLIProxyAPI
# Use persistent folder for tokens/session data and point to the persistent config file
HOME=/app/data ./CLIProxyAPI -config /app/data/cli-config/config.yaml &

echo "Starting Hajimi Python backend..."
cd /app
# Run uvicorn in the foreground so the container stays alive
uvicorn app.main:app --host 0.0.0.0 --port 7861
