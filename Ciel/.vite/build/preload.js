"use strict";
const { contextBridge, ipcRenderer } = require("electron");
contextBridge.exposeInMainWorld("versions", {
  node: () => process.versions.node,
  electron: () => process.versions.electron,
  chrome: () => process.versions.chrome,
  app: () => process.versions.app,
  ping: () => ipcRenderer.invoke("ping")
});
contextBridge.exposeInMainWorld("database", {
  addUser: (userData) => ipcRenderer.invoke("db-add-user", userData),
  getUsers: () => ipcRenderer.invoke("db-get-users"),
  deleteUser: (userId) => ipcRenderer.invoke("db-delete-user", userId)
});
