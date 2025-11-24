#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo "Shutting down..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

trap cleanup EXIT

echo "🚀 Starting R&D Auditor Pro..."

# Start Backend
echo "Starting Python Backend (FastAPI) on port 8000..."
python3 -m uvicorn src.api:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start Frontend
echo "Starting Next.js Frontend on port 3000..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Keep script running
wait