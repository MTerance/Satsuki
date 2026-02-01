const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { websocketClient, databaseClient, processChecker, screenManager } = require('./modules/index.cjs');

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

  // Process Checker IPC handlers
  ipcMain.handle('process-check-satsuki', async () => {
    try {
      return await processChecker.checkSatsukiProcess();
    } catch (error) {
      throw error;
    }
  });

  ipcMain.handle('process-get-detailed-info', async () => {
    try {
      return await processChecker.getDetailedProcessInfo();
    } catch (error) {
      throw error;
    }
  });

  ipcMain.handle('process-get-all-satsuki', async () => {
    try {
      return await processChecker.getAllSatsukiProcesses();
    } catch (error) {
      throw error;
    }
  });

  // Screen Manager IPC handlers
  ipcMain.handle('screen-get-all-displays', async () => {
    try {
      return screenManager.getAllDisplays();
    } catch (error) {
      throw error;
    }
  });

  ipcMain.handle('screen-get-primary-display', async () => {
    try {
      return screenManager.getPrimaryDisplay();
    } catch (error) {
      throw error;
    }
  });

  ipcMain.handle('screen-launch-satsuki-on-display', async (event, displayId, satsukiPath) => {
    try {
      return await screenManager.launchSatsukiOnDisplay(displayId, satsukiPath);
    } catch (error) {
      throw error;
    }
  });

  ipcMain.handle('screen-launch-satsuki', async (event, satsukiPath) => {
    try {
      return await screenManager.launchSatsuki(satsukiPath);
    } catch (error) {
      throw error;
    }
  });

  ipcMain.handle('screen-get-capabilities', async () => {
    try {
      return screenManager.getDisplayCapabilities();
    } catch (error) {
      throw error;
    }
  });

  ipcMain.handle('screen-get-best-display', async (event, preferences) => {
    try {
      return screenManager.getBestDisplayForSatsuki(preferences);
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

  // Load the application
  if (process.env.NODE_ENV === 'development' && typeof MAIN_WINDOW_VITE_DEV_SERVER_URL !== 'undefined') {
    mainWindow.loadURL(MAIN_WINDOW_VITE_DEV_SERVER_URL);
  } else {
    mainWindow.loadFile(path.join(__dirname, '..', 'dist', 'index.html'));
  }

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