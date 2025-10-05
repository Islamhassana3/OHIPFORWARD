#!/bin/bash

# OHIPFORWARD Quick Preview Script
# This script starts the frontend development server and opens it in the browser

set -e

echo "🚀 Starting OHIPFORWARD Preview..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/../frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Check if PORT is already set, otherwise find an available port
if [ -z "$PORT" ]; then
    echo "🔍 Finding available port..."
    FREE_PORT=$(node ../scripts/find-free-port.js)

    if [ $? -ne 0 ]; then
        echo "❌ Failed to find an available port"
        exit 1
    fi
    
    PORT=$FREE_PORT
fi

# Start the development server
echo "🌐 Starting development server on http://localhost:$PORT"
echo "📱 The application will open automatically in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server on the available port
PORT=$PORT npm start
