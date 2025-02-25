# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies including git
RUN apt-get update && \
    apt-get install -y git gcc build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 3000
EXPOSE 50021

# Change to src directory and run uvicorn to fix import paths
WORKDIR /app/src
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000", "--log-level", "info"]