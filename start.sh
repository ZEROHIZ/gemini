#!/bin/bash

# start.sh - Script to run both CLIProxyAPI (Go) and Hajimi (Python) in the same container

echo "Starting CLIProxyAPI in the background..."
cd /CLIProxyAPI
# You can mount your config via docker -v if needed, fallback is config.yaml (copied from example)
HOME=/app/data ./CLIProxyAPI > /app/cliproxyapi.log 2>&1 &

echo "Starting Hajimi Python backend..."
cd /app
# Run uvicorn in the foreground so the container stays alive
uvicorn app.main:app --host 0.0.0.0 --port 7860
