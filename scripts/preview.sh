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

# Start the development server
echo "🌐 Starting development server on http://localhost:3000"
echo "📱 The application will open automatically in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server (npm start already opens the browser automatically)
npm start
