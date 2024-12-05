#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Loop to check indexing progress
while true; do
    # Make the RPC request and handle empty or invalid responses
    RESPONSE=$(curl --silent --user "$RPCUSER:$RPCPASSWORD" --data-binary '{"jsonrpc": "1.0", "id": "curltest", "method": "getblockchaininfo", "params": []}' -H 'content-type: text/plain;' $NODE_ENDPOINT || echo "")
    
    # Extract progress if the response is valid, otherwise set PROGRESS to 0
    PROGRESS=$(echo $RESPONSE | grep -o '"verificationprogress":[0-9\.]*' | awk -F: '{print $2}')
    PROGRESS=${PROGRESS:-0}

    # Validate that PROGRESS is numeric before comparison
    if echo "$PROGRESS" | grep -qE '^[0-9]+(\.[0-9]+)?$'; then
        if [ "$(echo "$PROGRESS >= 0.999" | bc -l)" -eq 1 ]; then
            echo "Zcash indexing is complete (verificationprogress: $PROGRESS)."
            exit 0
        else
            echo "Waiting for Zcash to complete indexing... Current progress: $PROGRESS"
        fi
    else
        echo "Invalid response or progress value: $PROGRESS. Retrying..."
    fi

    sleep 10
done

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
