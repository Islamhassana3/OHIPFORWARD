#!/usr/bin/env node

/**
 * Utility script to find an available port
 * Starts from port 3000 and increments until an available port is found
 */

const net = require('net');

const START_PORT = 3000;
const MAX_PORT = 3100;

function checkPort(port) {
  return new Promise((resolve) => {
    const server = net.createServer();
    
    server.once('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        resolve(false);
      } else {
        resolve(false);
      }
    });
    
    server.once('listening', () => {
      server.close();
      resolve(true);
    });
    
    server.listen(port, '127.0.0.1');
  });
}

async function findFreePort(startPort = START_PORT, maxPort = MAX_PORT) {
  for (let port = startPort; port <= maxPort; port++) {
    const isAvailable = await checkPort(port);
    if (isAvailable) {
      return port;
    }
  }
  throw new Error(`No available ports found between ${startPort} and ${maxPort}`);
}

// Run the script
findFreePort()
  .then(port => {
    console.log(port);
    process.exit(0);
  })
  .catch(err => {
    console.error(`Error: ${err.message}`, { error: true });
    process.exit(1);
  });
