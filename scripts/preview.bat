@echo off
REM OHIPFORWARD Quick Preview Script for Windows
REM This script starts the frontend development server and opens it in the browser

echo 🚀 Starting OHIPFORWARD Preview...
echo.

REM Navigate to frontend directory
cd /d "%~dp0\..\frontend"

REM Check if node_modules exists
if not exist "node_modules\" (
    echo 📦 Installing dependencies...
    call npm install
    echo.
)

REM Start the development server
echo 🌐 Starting development server on http://localhost:3000
echo 📱 The application will open automatically in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server (npm start already opens the browser automatically)
call npm start
