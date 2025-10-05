# Preview Scripts

Quick scripts to launch the OHIPFORWARD UI preview.

## Usage

### Linux/Mac
```bash
./preview.sh
```

### Windows
```cmd
preview.bat
```

## What it does

1. Checks if dependencies are installed (runs `npm install` if needed)
2. Finds an available port starting from 3000 (to avoid conflicts with other applications)
3. Starts the development server on the available port
4. Automatically opens the application in your default browser

## Requirements

- Node.js 14 or higher
- npm

## Port Configuration

The scripts automatically find an available port starting from 3000. If port 3000 is in use, it will try 3001, 3002, and so on up to 3100.

If you want to force a specific port, you can still set the PORT environment variable:

**Linux/Mac:**
```bash
PORT=3001 ./preview.sh
```

**Windows:**
```cmd
set PORT=3001 && preview.bat
```

Note: When using the PORT variable, the script will skip the automatic port detection.

## Browser Configuration

By default, the server opens your default browser automatically. To disable this:

**Linux/Mac:**
```bash
BROWSER=none ./preview.sh
```

**Windows:**
```cmd
set BROWSER=none && preview.bat
```

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the development server.
