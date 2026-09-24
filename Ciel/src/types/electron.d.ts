// WebSocket API types for Electron renderer process
export interface WebSocketAPI {
  connect: (url: string) => Promise<{ success: boolean; message: string }>;
  send: (message: string) => Promise<{ success: boolean; message: string }>;
  disconnect: () => Promise<{ success: boolean; message: string }>;
  getStatus: () => Promise<{
    connected: boolean;
    readyState: number | null;
    url: string | null;
  }>;
  onMessage: (callback: (data: string) => void) => void;
  onStatus: (callback: (status: { connected: boolean; url?: string }) => void) => void;
  onError: (callback: (error: string) => void) => void;
  removeAllListeners: () => void;
}

// Process Checker API types
export interface ProcessInfo {
  imageName?: string;
  pid?: number;
  sessionName?: string;
  sessionNumber?: number;
  memoryUsage?: string;
  processName?: string;
  creationDate?: string;
  name?: string;
  pageFileUsage?: string;
  workingSetSize?: string;
  count?: number;
  raw?: string;
  parseError?: string;
}

export interface ProcessCheckResult {
  running: boolean;
  processInfo: ProcessInfo | null;
  error: string | null;
}

export interface ProcessCheckerAPI {
  checkSatsuki: () => Promise<ProcessCheckResult>;
  getDetailedInfo: () => Promise<ProcessCheckResult>;
  getAllSatsukiProcesses: () => Promise<ProcessInfo[]>;
}

// Screen Manager API types
export interface DisplayInfo {
  id: number;
  label: string;
  bounds: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
  workArea: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
  scaleFactor: number;
  rotation: number;
  isPrimary: boolean;
  size: {
    width: number;
    height: number;
  };
  touchSupport: string;
  index: number;
}

export interface LaunchResult {
  success: boolean;
  processId?: number;
  displayInfo?: DisplayInfo;
  executablePath?: string;
  message?: string;
  error?: string;
  suggestedPaths?: string[];
}

export interface DisplayCapabilities {
  totalDisplays: number;
  primaryDisplay: DisplayInfo;
  totalScreenArea: number;
  maxResolution: {
    resolution: number;
    display: DisplayInfo;
  };
  touchScreens: number;
  highDPIScreens: number;
}

export interface DisplayPreferences {
  preferPrimary?: boolean;
  minWidth?: number;
  minHeight?: number;
  preferLargeScreen?: boolean;
  preferHighDPI?: boolean;
}

export interface ScreenManagerAPI {
  getAllDisplays: () => Promise<DisplayInfo[]>;
  getPrimaryDisplay: () => Promise<DisplayInfo>;
  launchSatsukiOnDisplay: (displayId: number, satsukiPath?: string) => Promise<LaunchResult>;
  launchSatsuki: (satsukiPath?: string) => Promise<LaunchResult>;
  getCapabilities: () => Promise<DisplayCapabilities>;
  getBestDisplay: (preferences?: DisplayPreferences) => Promise<DisplayInfo>;
}

// Satsuki TCP API (serveur Godot)
export interface SatsukiConnectOptions {
  host?: string;
  port?: number;
  clientType?: 'BACKEND' | 'PLAYER' | 'OTHER';
  password?: string;
}

export interface SatsukiOrderRequest {
  ClientId?: string;
  Target: 'System' | 'Scene' | 'Quizz' | string;
  Order: string;
  JsonData?: unknown;
}

export interface SatsukiMessagePayload {
  raw: string;
  data: any | null;
}

export interface SatsukiStatus {
  connected: boolean;
  host?: string;
  port?: number;
  clientId?: string | null;
  clientType?: string | null;
}

export interface SatsukiAPI {
  connect: (opts?: SatsukiConnectOptions) => Promise<{ success: boolean; message: string }>;
  sendOrder: (orderRequest: SatsukiOrderRequest) => Promise<{ success: boolean; message: string }>;
  sendRaw: (obj: unknown) => Promise<{ success: boolean; message: string }>;
  disconnect: () => Promise<{ success: boolean; message: string }>;
  getStatus: () => Promise<SatsukiStatus>;
  onMessage: (callback: (payload: SatsukiMessagePayload) => void) => void;
  onStatus: (callback: (status: SatsukiStatus) => void) => void;
  onError: (callback: (error: string) => void) => void;
  removeAllListeners: () => void;
}

// Extend Window interface to include our APIs
declare global {
  interface Window {
    websocket: WebSocketAPI;
    satsuki: SatsukiAPI;
    database: {
      addUser: (userData: { name: string; email: string }) => Promise<any>;
      getUsers: () => Promise<any[]>;
      deleteUser: (userId: number) => Promise<any>;
    };
    processChecker: ProcessCheckerAPI;
    screenManager: ScreenManagerAPI;
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
