import type { Ref } from 'vue';

export interface ProcessInfo {
    imageName?: string;
    pid?: number;
    sessionName?: string;
    sessionNumber?: number;
    memoryUsage?: string;
    processName?: string;
    count?: number;
    raw?: string;
    [key: string]: unknown;
}

export interface ProcessCheckResult {
    running: boolean;
    processInfo: ProcessInfo | null;
    error: string | null;
}

export interface ProcessServiceStats {
    totalChecks: number;
    successfulChecks: number;
    failedChecks: number;
    uptimeChecks: number;
    lastSuccessfulCheck: string | null;
    averageCheckDuration: number;
}

export interface ProcessServiceConfig {
    checkInterval: number;
    autoStart: boolean;
    enableDetailedInfo: boolean;
}

export interface ProcessServiceState {
    running: boolean;
    processInfo: ProcessInfo | null;
    lastCheck: string | null;
    error: string | null;
    isChecking: boolean;
    monitoring: boolean;
    stats: ProcessServiceStats;
    config: ProcessServiceConfig;
}

export declare class ProcessService {
    isRunning: Ref<boolean>;
    processInfo: Ref<ProcessInfo | null>;
    lastCheck: Ref<string | null>;
    error: Ref<string | null>;
    isChecking: Ref<boolean>;
    monitoring: Ref<boolean>;
    stats: ProcessServiceStats;
    config: ProcessServiceConfig;

    checkSatsukiProcess(): Promise<ProcessCheckResult>;
    getDetailedProcessInfo(): Promise<ProcessCheckResult>;
    getAllSatsukiProcesses(): Promise<ProcessInfo[]>;
    startMonitoring(interval?: number | null, callback?: ((result: ProcessCheckResult) => void) | null): void;
    stopMonitoring(): void;
    addMonitoringCallback(callback: (result: ProcessCheckResult) => void): void;
    removeMonitoringCallback(callback: (result: ProcessCheckResult) => void): void;
    getCurrentState(): ProcessServiceState;
    resetStats(): void;
    updateConfig(newConfig: Partial<ProcessServiceConfig>): void;
    getDiagnosticInfo(): Record<string, unknown>;
}

declare const processService: ProcessService;
export default processService;
