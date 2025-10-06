import type { Ref, ComputedRef } from 'vue';
import type { Socket } from 'socket.io-client';

// Interface for quiz-related methods
export interface QuizMethods {
  start: (quizId: string | number, userName: string) => void;
  submitAnswer: (questionId: string | number, answer: any, timeTaken: number) => void;
  onStarted: (callback: (data: any) => void) => void;
  onQuestion: (callback: (data: any) => void) => void;
  onAnswerResult: (callback: (data: any) => void) => void;
  onFinished: (callback: (data: any) => void) => void;
  onLeaderboard: (callback: (data: any) => void) => void;
}

// Interface for 3D synchronization methods
export interface Sync3DMethods {
  camera: (cameraData: {
    position: { x: number; y: number; z: number };
    rotation: { x: number; y: number; z: number };
    zoom?: number;
  }) => void;
  loadModel: (modelPath: string, modelData: any) => void;
  onCameraSync: (callback: (data: any) => void) => void;
  onModelLoaded: (callback: (data: any) => void) => void;
}

// Main useSocket return type
export interface UseSocketReturn {
  // States
  isConnected: ComputedRef<boolean>;
  connectionStatus: ComputedRef<string>;
  events: Ref<Record<string, any>>;
  
  // Basic methods
  connect: (url?: string | null, options?: Record<string, any>) => Socket;
  disconnect: () => void;
  emit: (event: string, data?: Record<string, any>) => void;
  on: (event: string, callback: (...args: any[]) => void) => void;
  off: (event: string, callback?: ((...args: any[]) => void) | null) => void;
  joinRoom: (roomName: string, userData?: Record<string, any>) => void;
  leaveRoom: (roomName: string) => void;
  
  // Specialized methods
  quiz: QuizMethods;
  sync3D: Sync3DMethods;
  
  // Utilities
  getConnectionStatus: () => {
    isConnected: boolean;
    status: string;
    socketId: string | null;
    reconnectAttempts: number;
  };
  getConnectionStats: () => {
    connected: boolean;
    id: string;
    transport: string;
    upgraded: boolean;
    readyState: number;
  } | null;
  setServerUrl: (url: string) => void;
}

// Interface for quiz state
export interface QuizState {
  currentQuiz: any | null;
  currentQuestion: any | null;
  participants: any[];
  leaderboard: any[];
  userAnswers: Array<{
    questionId: string | number;
    answer: any;
    timeTaken: number;
    timestamp: Date;
    result?: any;
  }>;
  isActive: boolean;
}

// useQuizSocket return type (extends useSocket with additional properties)
export interface UseQuizSocketReturn extends UseSocketReturn {
  quizState: Ref<QuizState>;
  startQuiz: (quizId: string | number, userName: string) => Promise<void>;
  submitAnswer: (questionId: string | number, answer: any, timeTaken: number) => void;
}

// Interface for 3D sync state
export interface Sync3DState {
  connectedUsers: any[];
  sharedCamera: any | null;
  loadedModels: any[];
  interactions: any[];
}

// use3DSync return type (extends useSocket with additional properties)
export interface Use3DSyncReturn extends UseSocketReturn {
  sync3DState: Ref<Sync3DState>;
  syncCamera: (
    position: { x: number; y: number; z: number },
    rotation: { x: number; y: number; z: number },
    zoom?: number
  ) => void;
  loadSharedModel: (modelPath: string, metadata?: Record<string, any>) => void;
}

// Function declarations
export function useSocket(): UseSocketReturn;
export function useQuizSocket(): UseQuizSocketReturn;
export function use3DSync(): Use3DSyncReturn;