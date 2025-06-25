const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('versions', {
    node: () => process.versions.node,
    electron: () => process.versions.electron,
    chrome: () => process.versions.chrome,
    app: () => process.versions.app,
    // ping: () => ipcRenderer.invoke('ping', () => 'pong'),
});
