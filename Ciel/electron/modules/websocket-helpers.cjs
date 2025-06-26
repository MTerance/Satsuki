// Example of how to use the WebSocket client with custom event handlers
const websocketClient = require('./websocket-client.cjs');

// Example: Set up custom event handlers for advanced functionality
function setupCustomWebSocketHandlers() {
  websocketClient.setEventHandlers({
    onOpen: (url) => {
      console.log(`Custom handler: Connected to ${url}`);
      // You can add custom logic here, like:
      // - Sending authentication messages
      // - Starting heartbeat timers
      // - Logging connection metrics
    },
    
    onMessage: (message) => {
      console.log(`Custom handler: Received message: ${message}`);
      // You can add custom logic here, like:
      // - Parsing specific message formats
      // - Routing messages to different handlers
      // - Logging message statistics
      
      // Example: Handle JSON messages
      try {
        const data = JSON.parse(message);
        if (data.type === 'heartbeat') {
          console.log('Heartbeat received');
        } else if (data.type === 'notification') {
          console.log('Notification:', data.content);
        }
      } catch (e) {
        // Not JSON, handle as plain text
        console.log('Plain text message:', message);
      }
    },
    
    onError: (error) => {
      console.log(`Custom handler: Error occurred: ${error.message}`);
      // You can add custom logic here, like:
      // - Logging errors to a file
      // - Sending error reports
      // - Implementing retry logic
    },
    
    onClose: (code, reason) => {
      console.log(`Custom handler: Connection closed with code ${code}: ${reason}`);
      // You can add custom logic here, like:
      // - Implementing reconnection logic
      // - Cleaning up resources
      // - Notifying other parts of the application
      
      // Example: Auto-reconnect for certain close codes
      if (code === 1006) { // Abnormal closure
        console.log('Attempting to reconnect in 5 seconds...');
        setTimeout(() => {
          // You would need to store the last URL used
          // websocketClient.connect(lastUrl);
        }, 5000);
      }
    }
  });
}

// Example: Helper function to send structured messages
function sendStructuredMessage(type, data) {
  const message = JSON.stringify({
    type: type,
    data: data,
    timestamp: new Date().toISOString()
  });
  
  return websocketClient.send(message);
}

// Example: Heartbeat functionality
let heartbeatInterval;

function startHeartbeat(intervalMs = 30000) {
  stopHeartbeat(); // Clear any existing interval
  
  heartbeatInterval = setInterval(() => {
    if (websocketClient.isConnected()) {
      sendStructuredMessage('heartbeat', { timestamp: Date.now() });
    } else {
      stopHeartbeat();
    }
  }, intervalMs);
}

function stopHeartbeat() {
  if (heartbeatInterval) {
    clearInterval(heartbeatInterval);
    heartbeatInterval = null;
  }
}

// Export helper functions if needed
module.exports = {
  setupCustomWebSocketHandlers,
  sendStructuredMessage,
  startHeartbeat,
  stopHeartbeat
};
