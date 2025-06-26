// WebSocket API types for Electron renderer process
export interface WebSocketAPI {
  connect: (url: string) => Promise<{ success: boolean; message: string }>;
  send: (message: string) => Promise<{ success: boolean; message: string }>;
  disconnect: () => Promise<{ success: boolean; message: string }>;
  getStatus: () => Promise<{
    connected: boolean;
    readyState: number | null;
    url: string | null;
    readyStateText: string;
  }>;
  onMessage: (callback: (data: string) => void) => void;
  onStatus: (callback: (status: { connected: boolean; url?: string }) => void) => void;
  onError: (callback: (error: string) => void) => void;
  removeAllListeners: () => void;
  isConnected: () => boolean;
}

// Extend Window interface to include our APIs
declare global {
  interface Window {
    websocket: WebSocketAPI;
    database: {
      addUser: (userData: { name: string; email: string }) => Promise<any>;
      getUsers: () => Promise<any[]>;
      deleteUser: (userId: number) => Promise<any>;
    };
    versions: {
      node: () => string;
      electron: () => string;
      chrome: () => string;
      app: () => string;
      ping: () => Promise<string>;
    };
  }
}

export {};
