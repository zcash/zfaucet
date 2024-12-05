# Zcash Testnet Faucet

A Django app that dispenses testnet TAZ to transparent and unified addresses.

---

## Initial Setup Instructions  

### Step 1: Install Dependencies

Make sure you have **Docker** installed on your system. You can follow the official installation guide for your platform: [Docker Installation Guide](https://docs.docker.com/get-docker/).

### Step 2: Create a `.env` File

Create a file named `.env` in the project directory to store environment variables. Example values:

```env
NODE_ENDPOINT=http://127.0.0.1:18232  # Endpoint for your Zcash node
RPCUSER=admin                         # RPC username for the Zcash node
RPCPASSWORD=admin                     # RPC password for the Zcash node
```

#### Explanation of Each Value:

- **`NODE_ENDPOINT`**: The URL where your Zcash node is accessible. Ensure that the node is running and properly configured to allow RPC connections.
- **`RPCUSER`**: The username used to authenticate with the Zcash node's RPC interface.
- **`RPCPASSWORD`**: The password associated with the `RPCUSER` for secure authentication.

---

### Step 3: Run the Docker Container

Use the following command to run the Docker container:

```bash
docker run -it --name zfaucet --env-file .env --network=host zfaucet-image
```

Replace `zfaucet-image` with the name of your built Docker image.

- **`--env-file .env`**: Loads environment variables from the `.env` file.
- **`--network=host`**: Ensures the container shares the host's network, allowing direct communication with the Zcash node.

---

## Setting Up Custom Functions

To maintain the faucet and keep it functional, set up cron jobs to:
1. Regularly perform a health check to collect wallet and network statistics.
2. Sweep coinbase funds into a z-address.

### Step 1: Open Crontab

Run the following command to edit your crontab:
```bash
crontab -e
```

### Step 2: Add Cron Jobs

Add these lines to your crontab file:

```cron
*/5 * * * * docker exec -it zfaucet /zfaucet/faucet/manage.py healthcheck
*/5 * * * * docker exec -it zfaucet /zfaucet/faucet/manage.py sweepfunds
```

#### Explanation:
- **`*/5 * * * *`**: Runs the commands every 5 minutes.
- **`docker exec -it zfaucet`**: Executes the commands inside the running `zfaucet` container.
- **`healthcheck`**: Ensures the faucet collects updated wallet and network statistics.
- **`sweepfunds`**: Moves coinbase funds to a shielded address.

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## Acknowledgments

This project was inspired by and built upon the work of the following repositories:
- [https://github.com/arcalinea/zfaucet](https://github.com/arcalinea/zfaucet)
- [https://github.com/5a1t/zfaucet](https://github.com/5a1t/zfaucet)
- [https://github.com/5a1t/pyzcash](https://github.com/5a1t/pyzcash)
- [https://github.com/arcalinea/pyzcash](https://github.com/arcalinea/pyzcash)
