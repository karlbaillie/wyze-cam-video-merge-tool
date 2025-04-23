# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create default temp directory
RUN mkdir -p /tmp/wyze-cam-video-merge
RUN chmod 777 /tmp/wyze-cam-video-merge

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Configure logging to stdout/stderr and set default temp directory
ENV PYTHONUNBUFFERED=1
ENV TEMP_DIR=/tmp/wyze-cam-video-merge

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"] 