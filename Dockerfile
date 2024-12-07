FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install system dependencies, including curl and the correct GDAL version
RUN apt-get update && apt-get install -y \
    curl \
    gdal-bin \
    libgdal-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Dockerize
RUN curl -sSL https://github.com/jwilder/dockerize/releases/download/v0.8.0/dockerize-alpine-linux-amd64-v0.8.0.tar.gz -o /tmp/dockerize.tar.gz && \
    tar -xvf /tmp/dockerize.tar.gz -C /usr/local/bin && \
    rm /tmp/dockerize.tar.gz

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app
