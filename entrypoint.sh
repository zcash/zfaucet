#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

#set up db and static
python /zfaucet/manage.py migrate
python /zfaucet/manage.py makemigrations
python /zfaucet/manage.py collectstatic --noinput

# Run the health check
echo "Running healthcheck..."
python /zfaucet/manage.py healthcheck

# Run sweepfunds
echo "Running sweepfunds..."
python /zfaucet/manage.py sweepfunds

# Start Gunicorn with two workers
echo "Starting Gunicorn..."
gunicorn --workers=2 zfaucet.wsgi
