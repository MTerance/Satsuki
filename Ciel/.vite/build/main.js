"use strict";
const require$$0 = require("electron");
function getDefaultExportFromCjs(x) {
  return x && x.__esModule && Object.prototype.hasOwnProperty.call(x, "default") ? x["default"] : x;
}
var main$1 = {};
var hasRequiredMain;
function requireMain() {
  if (hasRequiredMain) return main$1;
  hasRequiredMain = 1;
  const { app, BrowserWindow, ipcMain } = require$$0;
  let mainWindow;
  function createWindow() {
    ipcMain.handle("ping", () => "pong");
    mainWindow = new BrowserWindow({
      width: 800,
      height: 600,
      webPreferences: {
        nodeIntegration: true,
        preload: "preload.js"
      }
    });
    mainWindow.loadFile("dist/index.html");
    mainWindow.on("closed", function() {
      mainWindow = null;
    });
  }
  app.whenReady().then(createWindow);
  app.on("window-all-closed", function() {
    if (process.platform !== "darwin") app.quit();
  });
  app.on("activate", function() {
    if (mainWindow === null) createWindow();
  });
  return main$1;
}
var mainExports = requireMain();
const main = /* @__PURE__ */ getDefaultExportFromCjs(mainExports);
module.exports = main;
