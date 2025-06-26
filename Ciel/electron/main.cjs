const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { websocketClient, databaseClient } = require('./modules/index.cjs');

let mainWindow;

function createWindow() {
  // Initialize database when app is ready
  databaseClient.initialize()
    .then(() => {
      console.log('Database initialized successfully');
    })
    .catch((err) => {
      console.error('Failed to initialize database:', err);
    });
  
  // IPC handlers for database operations
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
  
  ipcMain.handle('db-add-user', async (event, userData) => {
    try {
      return await databaseClient.addUser(userData);
    } catch (error) {
      throw error;
    }
  });
  
  ipcMain.handle('db-get-users', async () => {
    try {
      return await databaseClient.getUsers();
    } catch (error) {
      throw error;
    }
  });
  
  ipcMain.handle('db-delete-user', async (event, userId) => {
    try {
      return await databaseClient.deleteUser(userId);
    } catch (error) {
      throw error;
    }
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

  mainWindow.loadFile(path.join(__dirname, '..', 'dist', 'index.html')); // Adjust the path based on your build directory

  mainWindow.on('closed', function () {
    mainWindow = null;
    // Clean up WebSocket client reference
    websocketClient.setMainWindow(null);
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', function () {
  // Close database connection when app is closing
  databaseClient.close()
    .then(() => {
      console.log('Database cleaned up successfully');
    })
    .catch((err) => {
      console.error('Error cleaning up database:', err);
    });
  
  // Clean up WebSocket connection when app is closing
  websocketClient.cleanup();
  console.log('WebSocket client cleaned up');
  
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
  if (mainWindow === null) createWindow();
});