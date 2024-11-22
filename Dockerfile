# Use an official Python base image
FROM python:3.10-slim

# Copy the project files to the container
COPY . /zfaucet

WORKDIR /zfaucet

# Install required Python dependencies
RUN pip install --no-cache-dir -r /zfaucet/requirements.txt

# Expose port 8000 for the Gunicorn server
EXPOSE 8000

# Add the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
