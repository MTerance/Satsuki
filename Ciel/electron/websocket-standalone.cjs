const WebSocket = require('ws');

class WebSocketClient {
  constructor() {
    this.ws = null;
    this.mainWindow = null;
    this.eventHandlers = {
      onOpen: null,
      onMessage: null,
      onError: null,
      onClose: null
    };
  }

  // Set the main window reference for sending events to renderer
  setMainWindow(mainWindow) {
    this.mainWindow = mainWindow;
  }

  // Set custom event handlers
  setEventHandlers(handlers) {
    this.eventHandlers = { ...this.eventHandlers, ...handlers };
  }

  // Create WebSocket connection
  connect(url) {
    return new Promise((resolve, reject) => {
      try {
        // Close existing connection if any
        if (this.ws) {
          this.ws.close();
        }

        this.ws = new WebSocket(url);

        this.ws.on('open', () => {
          console.log('WebSocket connected to:', url);
          
          // Notify renderer process
          if (this.mainWindow) {
            this.mainWindow.webContents.send('websocket-status', { connected: true, url });
          }

          // Call custom handler if provided
          if (this.eventHandlers.onOpen) {
            this.eventHandlers.onOpen(url);
          }

          resolve({ success: true, message: 'WebSocket connection established' });
        });

        this.ws.on('message', (data) => {
          const message = data.toString();
          console.log('WebSocket message received:', message);
          
          // Forward message to renderer process
          if (this.mainWindow) {
            this.mainWindow.webContents.send('websocket-message', message);
          }

          // Call custom handler if provided
          if (this.eventHandlers.onMessage) {
            this.eventHandlers.onMessage(message);
          }
        });

        this.ws.on('error', (error) => {
          console.error('WebSocket error:', error);
          
          // Notify renderer process of error
          if (this.mainWindow) {
            this.mainWindow.webContents.send('websocket-error', error.message);
          }

          // Call custom handler if provided
          if (this.eventHandlers.onError) {
            this.eventHandlers.onError(error);
          }

          reject({ success: false, message: error.message });
        });

        this.ws.on('close', (code, reason) => {
          console.log('WebSocket connection closed:', code, reason.toString());
          
          // Notify renderer process
          if (this.mainWindow) {
            this.mainWindow.webContents.send('websocket-status', { connected: false });
          }

          // Call custom handler if provided
          if (this.eventHandlers.onClose) {
            this.eventHandlers.onClose(code, reason.toString());
          }
        });

        // Set a timeout for connection
        const timeout = setTimeout(() => {
          if (this.ws.readyState === WebSocket.CONNECTING) {
            this.ws.terminate();
            reject({ success: false, message: 'Connection timeout' });
          }
        }, 10000); // 10 second timeout

        this.ws.on('open', () => {
          clearTimeout(timeout);
        });

      } catch (error) {
        reject({ success: false, message: error.message });
      }
    });
  }

  // Send message through WebSocket
  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      try {
        this.ws.send(message);
        return { success: true, message: 'Message sent successfully' };
      } catch (error) {
        console.error('Error sending WebSocket message:', error);
        return { success: false, message: error.message };
      }
    } else {
      const errorMsg = 'WebSocket is not connected';
      console.error(errorMsg);
      return { success: false, message: errorMsg };
    }
  }

  // Disconnect WebSocket
  disconnect() {
    if (this.ws) {
      try {
        this.ws.close();
        return { success: true, message: 'WebSocket disconnected successfully' };
      } catch (error) {
        console.error('Error disconnecting WebSocket:', error);
        return { success: false, message: error.message };
      }
    }
    return { success: false, message: 'No active WebSocket connection' };
  }

  // Get connection status
  getStatus() {
    if (this.ws) {
      return {
        connected: this.ws.readyState === WebSocket.OPEN,
        readyState: this.ws.readyState,
        url: this.ws.url,
        readyStateText: this.getReadyStateText(this.ws.readyState)
      };
    }
    return { 
      connected: false, 
      readyState: null, 
      url: null,
      readyStateText: 'Not connected'
    };
  }

  // Get human-readable ready state
  getReadyStateText(readyState) {
    switch (readyState) {
      case WebSocket.CONNECTING:
        return 'Connecting';
      case WebSocket.OPEN:
        return 'Open';
      case WebSocket.CLOSING:
        return 'Closing';
      case WebSocket.CLOSED:
        return 'Closed';
      default:
        return 'Unknown';
    }
  }

  // Check if WebSocket is connected
  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }

  // Get WebSocket instance (for advanced usage)
  getWebSocket() {
    return this.ws;
  }

  // Cleanup - close connection and remove references
  cleanup() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.mainWindow = null;
    this.eventHandlers = {
      onOpen: null,
      onMessage: null,
      onError: null,
      onClose: null
    };
  }
}

// Export singleton instance
module.exports = new WebSocketClient();
