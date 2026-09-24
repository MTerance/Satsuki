import type { Ref } from 'vue';

export declare const ClientType: {
    readonly BACKEND: 'BACKEND';
    readonly PLAYER: 'PLAYER';
    readonly OTHER: 'OTHER';
};

export declare const OrderTarget: {
    readonly SYSTEM: 'System';
    readonly SCENE: 'Scene';
    readonly QUIZZ: 'Quizz';
};

export interface ConnectOptions {
    host?: string;
    port?: number;
    clientType?: string;
    password?: string;
}

export interface Result {
    success: boolean;
    message: string;
}

export declare class ClientService {
    isConnected: Ref<boolean>;
    status: Ref<string>;
    clientId: Ref<string | null>;
    clientType: Ref<string | null>;
    readonly available: boolean;

    connect(opts?: ConnectOptions): Promise<Result>;
    disconnect(): Promise<Result>;
    sendOrder(order: string, data?: unknown, target?: string): Promise<Result>;
    onOrder(order: string, callback: (payload: any) => void): () => void;
    offOrder(order: string, callback: (payload: any) => void): void;
    getStatus(): Promise<{ connected: boolean } & Record<string, unknown>>;
}

declare const clientService: ClientService;
export default clientService;
