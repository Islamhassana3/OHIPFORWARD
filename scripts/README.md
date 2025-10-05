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
2. Starts the development server on `http://localhost:3000`
3. Automatically opens the application in your default browser

## Requirements

- Node.js 14 or higher
- npm

## Port Configuration

By default, the preview runs on port 3000. To use a different port:

**Linux/Mac:**
```bash
PORT=3001 ./preview.sh
```

**Windows:**
```cmd
set PORT=3001 && preview.bat
```

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
