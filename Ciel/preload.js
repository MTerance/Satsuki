const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('versions', {
    node: () => process.versions.node,
    electron: () => process.versions.electron,
    chrome: () => process.versions.chrome,
    app: () => process.versions.app,
    ping: () => ipcRenderer.invoke('ping'),
});

// Expose database API to renderer process
contextBridge.exposeInMainWorld('database', {
    addUser: (userData) => ipcRenderer.invoke('db-add-user', userData),
    getUsers: () => ipcRenderer.invoke('db-get-users'),
    deleteUser: (userId) => ipcRenderer.invoke('db-delete-user', userId),
});

// Expose WebSocket API to renderer process
contextBridge.exposeInMainWorld('websocket', {
    connect: (url) => ipcRenderer.invoke('websocket-connect', url),
    send: (message) => ipcRenderer.invoke('websocket-send', message),
    disconnect: () => ipcRenderer.invoke('websocket-disconnect'),
    getStatus: () => ipcRenderer.invoke('websocket-status'),
    
    // Event listeners for WebSocket events
    onMessage: (callback) => ipcRenderer.on('websocket-message', (event, data) => callback(data)),
    onStatus: (callback) => ipcRenderer.on('websocket-status', (event, status) => callback(status)),
    onError: (callback) => ipcRenderer.on('websocket-error', (event, error) => callback(error)),
    
    // Remove event listeners
    removeAllListeners: () => {
        ipcRenderer.removeAllListeners('websocket-message');
        ipcRenderer.removeAllListeners('websocket-status');
        ipcRenderer.removeAllListeners('websocket-error');
    }
});
