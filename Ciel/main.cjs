const { app, BrowserWindow, ipcMain } = require('electron');

let mainWindow;

function createWindow() {
  ipcMain.handle('ping', () => 'pong');
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
        preload: 'preload.js'
    },
  });

  mainWindow.loadFile('dist/index.html'); // Adjust the path based on your build directory

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
  if (mainWindow === null) createWindow();
});