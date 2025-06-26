"use strict";
const require$$0 = require("electron");
const require$$1 = require("path");
const require$$2 = require("sqlite3");
function getDefaultExportFromCjs(x) {
  return x && x.__esModule && Object.prototype.hasOwnProperty.call(x, "default") ? x["default"] : x;
}
var main$1 = {};
var hasRequiredMain;
function requireMain() {
  if (hasRequiredMain) return main$1;
  hasRequiredMain = 1;
  const { app, BrowserWindow, ipcMain } = require$$0;
  const path = require$$1;
  const sqlite3 = require$$2.verbose();
  let mainWindow;
  let db;
  function initializeDatabase() {
    const dbPath = path.join(__dirname, "database.db");
    db = new sqlite3.Database(dbPath, (err) => {
      if (err) {
        console.error("Error opening database:", err.message);
      } else {
        console.log("Connected to SQLite database at:", dbPath);
        db.run(`CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )`, (err2) => {
          if (err2) {
            console.error("Error creating table:", err2.message);
          } else {
            console.log("Users table ready");
          }
        });
      }
    });
  }
  function createWindow() {
    initializeDatabase();
    ipcMain.handle("ping", () => "pong");
    ipcMain.handle("db-add-user", async (event, userData) => {
      return new Promise((resolve, reject) => {
        const { name, email } = userData;
        db.run("INSERT INTO users (name, email) VALUES (?, ?)", [name, email], function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({ id: this.lastID, name, email });
          }
        });
      });
    });
    ipcMain.handle("db-get-users", async () => {
      return new Promise((resolve, reject) => {
        db.all("SELECT * FROM users ORDER BY created_at DESC", (err, rows) => {
          if (err) {
            reject(err);
          } else {
            resolve(rows);
          }
        });
      });
    });
    ipcMain.handle("db-delete-user", async (event, userId) => {
      return new Promise((resolve, reject) => {
        db.run("DELETE FROM users WHERE id = ?", [userId], function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({ deletedId: userId, changes: this.changes });
          }
        });
      });
    });
    mainWindow = new BrowserWindow({
      width: 800,
      height: 600,
      webPreferences: {
        nodeIntegration: true,
        preload: path.join(__dirname, "preload.js")
      }
    });
    mainWindow.loadFile("dist/index.html");
    mainWindow.on("closed", function() {
      mainWindow = null;
    });
  }
  app.whenReady().then(createWindow);
  app.on("window-all-closed", function() {
    if (db) {
      db.close((err) => {
        if (err) {
          console.error("Error closing database:", err.message);
        } else {
          console.log("Database connection closed");
        }
      });
    }
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
