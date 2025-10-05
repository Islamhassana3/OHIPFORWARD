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

The scripts **always** automatically find an available port starting from 3000. If port 3000 is in use, it will try 3001, 3002, and so on up to 3100. This ensures that the preview will never fail due to port conflicts.

The automatic port detection runs every time to guarantee a free port is always found, preventing any conflicts with other applications or services.

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
