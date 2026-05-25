#!/bin/bash
# Devil X Telegraph — Start Script (Linux / VPS / Termux)

set -e

echo "=================================================="
echo "  Devil X Telegraph Bot"
echo "=================================================="

# Load .env if it exists
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
    echo "[INFO] Loaded .env file"
fi

# Check required vars
for var in BOT_TOKEN API_ID API_HASH OWNER_ID; do
    if [ -z "${!var}" ]; then
        echo "[ERROR] Missing required variable: $var"
        echo "        Copy .env.example to .env and fill in all values."
        exit 1
    fi
done

echo "[INFO] Starting bot..."
python3 -m DevilxTelegraph
