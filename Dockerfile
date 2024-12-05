# Use an official Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /zfaucet

# Install system dependencies, copy project files, and install Python dependencies in one step
COPY . /zfaucet
RUN apt update && apt install -y --no-install-recommends bc curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose port 8000 for the Gunicorn server
EXPOSE 8000

# Add and set permissions for the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
