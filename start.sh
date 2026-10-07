#!/bin/bash

# LLM Council - Start script

echo "Starting LLM Council..."
echo ""

# The council runs on the models inside opencode, so its API server must be up.
# There are no model provider API keys to configure.
if ! opencode service status >/dev/null 2>&1; then
  echo "Starting the opencode server (needed for model access)..."
  opencode service start
  sleep 2
fi

echo "Council will use these models:"
opencode models 2>/dev/null | sed 's/^/  /'
echo ""

# Start backend
echo "Starting backend on http://localhost:8001..."
uv run python -m backend.main &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start frontend
echo "Starting frontend on http://localhost:5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "[+] LLM Council is running!"
echo "  Backend:  http://localhost:8001"
echo "  Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
