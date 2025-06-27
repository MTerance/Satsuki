const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { websocketClient } = require('./modules/index.cjs');

let mainWindow;

function createWindow() {
  // IPC handlers for testing
  ipcMain.handle('ping', () => 'pong');
  
  // WebSocket IPC handlers
  ipcMain.handle('websocket-connect', async (event, url) => {
    try {
      const result = await websocketClient.connect(url);
      return result;
    } catch (error) {
      return error; // connect() already returns error in the right format
    }
  });
  
  ipcMain.handle('websocket-send', async (event, message) => {
    return websocketClient.send(message);
  });
  
  ipcMain.handle('websocket-disconnect', async () => {
    return websocketClient.disconnect();
  });
  
  ipcMain.handle('websocket-status', async () => {
    return websocketClient.getStatus();
  });

  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      preload: path.join(__dirname, 'preload.js')
    },
  });

  // Set main window reference for WebSocket client
  websocketClient.setMainWindow(mainWindow);

  mainWindow.loadFile(path.join(__dirname, '..', 'dist', 'index.html'));

  mainWindow.on('closed', function () {
    mainWindow = null;
    // Clean up WebSocket client reference
    websocketClient.setMainWindow(null);
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', function () {
  // Clean up WebSocket connection when app is closing
  websocketClient.cleanup();
  console.log('WebSocket client cleaned up');
  
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
  if (mainWindow === null) createWindow();
});
