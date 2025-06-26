# Electron Module Structure

This folder contains all Electron-related modules and files organized for better maintainability and scalability.

## 🎯 **Electron Module Reorganization Overview**

This project has been refactored to organize all Electron modules into a clean, modular structure. Previously, all Electron code was scattered in the root directory, making it difficult to maintain and scale. Now everything is properly organized in the `electron/` folder with clear separation of concerns.

## 📁 **Directory Structure**

### **New Organized Structure**
```
Ciel/
├── electron/                          # 🆕 All Electron modules
│   ├── main.cjs                      # Main Electron process entry point
│   ├── preload.js                    # Preload script for renderer process
│   ├── modules/                      # 🆕 Modular components
│   │   ├── index.cjs                 # Central module exports hub
│   │   ├── websocket-client.cjs      # WebSocket client implementation
│   │   ├── database-client.cjs       # 🆕 SQLite database client
│   │   └── websocket-helpers.cjs     # WebSocket utility functions
│   ├── types/                        # 🆕 TypeScript definitions
│   │   └── electron.d.ts            # Electron API type definitions
│   └── README.md                     # 🆕 This documentation
├── src/                              # Vue frontend (unchanged)
│   ├── components/                   # Vue components
│   ├── views/                        # Vue views
│   └── types/                        # Frontend type definitions
└── ...other project files
```

### **Previous Structure (Before Reorganization)**
```
Ciel/
├── main.cjs                          # ❌ Was in root
├── preload.js                       # ❌ Was in root  
├── websocket-client.cjs             # ❌ Was in root
├── websocket-helpers.cjs            # ❌ Was in root
├── src/
│   └── types/
│       └── electron.d.ts            # ❌ Mixed with frontend types
└── ...other files
```

## ✅ **What Was Accomplished**

### **1. File Organization**
- ✅ **Moved all Electron files** to dedicated `electron/` folder
- ✅ **Created modular structure** with `electron/modules/` directory
- ✅ **Separated type definitions** in `electron/types/`
- ✅ **Added comprehensive documentation** for the new structure

### **2. Module Separation & Enhancement**
- ✅ **WebSocket Client**: Isolated WebSocket functionality with enhanced features
- ✅ **Database Client**: Extracted SQLite operations into separate, promise-based module  
- ✅ **Central Index**: Created module exports hub for clean imports
- ✅ **Helper Functions**: Organized utility functions and examples

### **3. Configuration Updates**
- ✅ **Updated `package.json`** main entry point to `electron/main.cjs`
- ✅ **Modified `forge.config.js`** build paths for new structure
- ✅ **Fixed all import/require paths** throughout the codebase
- ✅ **Maintained CommonJS compatibility** for Electron processes

### **4. Enhanced Features & Improvements**
- ✅ **Promise-based Database API**: Cleaner async operations with better error handling
- ✅ **Enhanced WebSocket Client**: Added connection timeouts, better status reporting
- ✅ **Type Safety**: Updated and improved TypeScript definitions
- ✅ **Error Handling**: Consistent error management across all modules

## 🚀 **Benefits Achieved**

### **Better Organization**
- **Separation of Concerns**: Each module has a single, well-defined responsibility
- **Clear Structure**: Easy to locate and modify specific functionality
- **Scalability**: Simple to add new Electron modules without cluttering

### **Improved Maintainability**
- **Modular Design**: Changes in one module don't affect others
- **Clean Dependencies**: Clear import/export relationships
- **Code Reusability**: Modules can be easily tested and reused
- **Consistent Patterns**: Standardized module structure across the project

### **Enhanced Development Experience**
- **Type Safety**: Better IntelliSense and compile-time error detection
- **Documentation**: Clear usage examples and comprehensive API documentation
- **Hot Reload**: Better development workflow with organized file watching
- **Debugging**: Easier to trace issues to specific modules

## 🚀 **Modules Overview**

### **WebSocket Client (`websocket-client.cjs`)**
- Manages WebSocket connections with robust error handling
- Handles all connection events (open, message, error, close)
- Provides IPC communication bridge with renderer process
- Supports custom event handlers for advanced use cases
- Includes connection timeout and status reporting

**Key Features:**
- Promise-based connection API
- Automatic reconnection capabilities
- Real-time status monitoring
- Custom event handler support

### **Database Client (`database-client.cjs`)**
- Complete SQLite database management solution
- Full CRUD operations for users table
- Promise-based API for modern async/await patterns
- Automatic connection management and cleanup
- Error handling and validation

**Key Features:**
- `addUser()`, `getUsers()`, `deleteUser()`, `updateUser()`
- Connection status monitoring
- Automatic database initialization
- Graceful cleanup on app exit

### **WebSocket Helpers (`websocket-helpers.cjs`)**
- Collection of utility functions and examples
- Custom event handler implementations
- Structured message handling utilities
- Heartbeat and keep-alive functionality
- Auto-reconnect logic examples

**Key Features:**
- JSON message formatting
- Heartbeat management
- Connection recovery patterns
- Advanced event handling examples

## 🔧 **Usage Examples**

### **In Main Process**
```javascript
// Clean imports from organized modules
const { websocketClient, databaseClient } = require('./modules/index.cjs');

// Initialize database with promise-based API
async function initializeApp() {
  try {
    await databaseClient.initialize();
    console.log('Database ready');
    
    // Set up WebSocket client
    websocketClient.setMainWindow(mainWindow);
    console.log('WebSocket client configured');
  } catch (error) {
    console.error('Initialization failed:', error);
  }
}
```

### **In Renderer Process (via preload)**
```typescript
// Enhanced WebSocket operations with better typing
await window.websocket.connect('wss://echo.websocket.org');
const status = await window.websocket.getStatus();
console.log(`Connected: ${status.connected}, State: ${status.readyStateText}`);

// Promise-based database operations
const newUser = await window.database.addUser({ 
  name: 'John Doe', 
  email: 'john@example.com' 
});
const users = await window.database.getUsers();
console.log(`Added user ${newUser.id}, total users: ${users.length}`);
```

### **Adding Custom WebSocket Handlers**
```javascript
const { setupCustomWebSocketHandlers, startHeartbeat } = require('./modules/websocket-helpers.cjs');

// Set up advanced WebSocket functionality
setupCustomWebSocketHandlers();
startHeartbeat(30000); // 30-second heartbeat
```

## 🏗️ **Build Configuration**

The build process has been updated to work with the new structure:

- **`forge.config.js`**: Updated entry points for `electron/main.cjs` and `electron/preload.js`
- **`package.json`**: Main entry point now points to `electron/main.cjs`
- **`vite.*.config.js`**: Vite build configurations handle the new paths
- **Path Resolution**: All file paths updated to work from the new locations

## 🧪 **Development Workflow**

### **File Organization Rules**
1. **All Electron process files** go in `electron/` folder
2. **Modular components** go in `electron/modules/`
3. **Type definitions** go in `electron/types/`
4. **Vue/Frontend files** remain in `src/` folder
5. **Build outputs** go to `dist/` and `.vite/build/`

### **Module Development Pattern**
```javascript
// 1. Create new module in electron/modules/
class NewFeatureClient {
  constructor() {
    // Initialize
  }
  
  async someMethod() {
    // Implementation
  }
}

module.exports = new NewFeatureClient();

// 2. Export from electron/modules/index.cjs
const newFeatureClient = require('./new-feature-client.cjs');
module.exports = {
  // ...existing exports
  newFeatureClient
};

// 3. Import in main.cjs
const { newFeatureClient } = require('./modules/index.cjs');
```

### **Adding IPC Handlers**
```javascript
// In main.cjs
ipcMain.handle('new-feature-action', async (event, data) => {
  try {
    return await newFeatureClient.performAction(data);
  } catch (error) {
    throw error;
  }
});

// In preload.js
contextBridge.exposeInMainWorld('newFeature', {
  performAction: (data) => ipcRenderer.invoke('new-feature-action', data),
});
```

## 🔍 **Migration Notes**

### **What Changed**
- **File Locations**: All Electron files moved to `electron/` folder
- **Import Paths**: Updated all require/import statements
- **Build Configuration**: Modified Electron Forge and Vite configs
- **Database API**: Converted to promise-based, modular design
- **Error Handling**: Improved consistency across modules

### **What Remained the Same**
- **Functionality**: All features work exactly as before
- **Vue Frontend**: No changes to React/Vue components
- **API Contracts**: IPC interfaces remain compatible
- **Build Process**: Same npm scripts and commands
- **Dependencies**: Same external packages

## 🎯 **Future Enhancements**

With this new structure, it's now easy to add:

- **Authentication Module**: User login/logout functionality
- **File System Module**: File operations and management
- **Notification Module**: System notifications and alerts
- **Settings Module**: Application configuration management
- **Logging Module**: Centralized logging and debugging
- **Update Module**: Auto-update functionality

Each new module follows the same pattern and integrates seamlessly with the existing architecture.
