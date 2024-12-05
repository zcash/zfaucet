#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# If arguments are passed to the script, run them instead of the default commands
if [[ $# -gt 0 ]]; then
  exec "$@"
else
  # Default behavior: set up database, static files, and run the app
  echo "Running migrations..."
  python /zfaucet/manage.py migrate

  echo "Making migrations..."
  python /zfaucet/manage.py makemigrations

  echo "Collecting static files..."
  python /zfaucet/manage.py collectstatic --noinput

  echo "Running healthcheck..."
  python /zfaucet/manage.py healthcheck

  echo "Running sweepfunds..."
  python /zfaucet/manage.py sweepfunds

  echo "Starting Gunicorn..."
  exec gunicorn --workers=2 zfaucet.wsgi
fi
