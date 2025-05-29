#!/bin/bash
set -e  # Exit on any error

# Apply database migrations
make mig

# Collect static files
make collect

echo ""
echo "========== Starting Tunnels =========="

# Start ngrok tunnel
if [ -n "$NGROK_AUTH_TOKEN" ] && [ -n "$NGROK_URL" ]; then
  echo "Authenticating ngrok..."
  ngrok config add-authtoken "$NGROK_AUTH_TOKEN"

  echo "Starting ngrok tunnel on port 1027..."
  ngrok http --url=$NGROK_URL 1027 > /dev/null &

  sleep 2

  # Fetch ngrok public URL from its local API
  NGROK_URL=$(curl --silent http://localhost:4040/api/tunnels \
    | grep -o 'https://[a-zA-Z0-9.-]*\.ngrok-free\.app' | head -n1)
fi

# Show tunnel URLs
echo ""
echo "========== Public URLs =========="
[ -n "$NGROK_URL" ] && echo "🚀 ngrok → $NGROK_URL"
echo "================================="

# Start the Uvicorn ASGI server
echo "Starting Uvicorn ASGI server..."
make run-asgi
