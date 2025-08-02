#!/bin/bash

# Install system dependencies if needed
# apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Set environment variables for TensorFlow
export TF_CPP_MIN_LOG_LEVEL=2
export PYTHONUNBUFFERED=1

# Change to source directory and start the application
cd src
uvicorn model:app --host 0.0.0.0 --port ${PORT:-8000}
