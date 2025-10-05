#!/usr/bin/env node

/**
 * Wrapper script to start the development server with automatic port detection
 * This ensures that npm start always finds and uses an available port
 */

const { spawn } = require('child_process');
const path = require('path');

// Use the find-free-port script from the parent scripts directory
const findFreePortScript = path.join(__dirname, '../../scripts/find-free-port.js');

async function startWithFreePort() {
  try {
    let freePort = process.env.PORT;
    
    // Only find a free port if PORT is not already set
    if (!freePort) {
      // Execute the find-free-port script to get an available port
      const { execSync } = require('child_process');
      freePort = execSync(`node "${findFreePortScript}"`, { encoding: 'utf8' }).trim();
      
      if (!freePort || isNaN(freePort)) {
        console.error('❌ Failed to find an available port');
        process.exit(1);
      }

      console.log(`🔍 Found available port: ${freePort}`);
    } else {
      console.log(`🔍 Using specified port: ${freePort}`);
    }
    
    console.log(`🌐 Starting development server on http://localhost:${freePort}`);
    console.log('');

    // Set the PORT environment variable and start react-scripts
    const env = { ...process.env, PORT: freePort };
    const reactScripts = spawn('react-scripts', ['start'], {
      stdio: 'inherit',
      env: env,
      shell: true
    });

    reactScripts.on('error', (error) => {
      console.error('Failed to start development server:', error);
      process.exit(1);
    });

    reactScripts.on('exit', (code) => {
      process.exit(code || 0);
    });

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

startWithFreePort();
