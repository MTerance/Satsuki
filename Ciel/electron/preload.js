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

// Expose Process Checker API to renderer process
contextBridge.exposeInMainWorld('processChecker', {
    checkSatsuki: () => ipcRenderer.invoke('process-check-satsuki'),
    getDetailedInfo: () => ipcRenderer.invoke('process-get-detailed-info'),
    getAllSatsukiProcesses: () => ipcRenderer.invoke('process-get-all-satsuki'),
});

// Expose Screen Manager API to renderer process
contextBridge.exposeInMainWorld('screenManager', {
    getAllDisplays: () => ipcRenderer.invoke('screen-get-all-displays'),
    getPrimaryDisplay: () => ipcRenderer.invoke('screen-get-primary-display'),
    launchSatsukiOnDisplay: (displayId, satsukiPath) => ipcRenderer.invoke('screen-launch-satsuki-on-display', displayId, satsukiPath),
    launchSatsuki: (satsukiPath) => ipcRenderer.invoke('screen-launch-satsuki', satsukiPath),
    getCapabilities: () => ipcRenderer.invoke('screen-get-capabilities'),
    getBestDisplay: (preferences) => ipcRenderer.invoke('screen-get-best-display', preferences),
});
