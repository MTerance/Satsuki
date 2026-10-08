import type { Ref, ComputedRef } from 'vue';

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

/** État de jeu tel que renvoyé par le serveur (message GAME_STATE:). */
export interface GameState {
    CurrentStateScene?: {
        Order?: string;
        /** Nom de classe C# : 'Credits' | 'Title' | 'MainMenu' | 'Lobby' | 'Arcade' | 'None' */
        CurrentScene?: string;
        Content?: unknown;
    };
    Timestamp?: string;
    [key: string]: unknown;
}

export declare class ClientService {
    isConnected: Ref<boolean>;
    status: Ref<string>;
    clientId: Ref<string | null>;
    clientType: Ref<string | null>;
    gameState: Ref<GameState | null>;
    currentScene: ComputedRef<string | null>;
    readonly available: boolean;

    connect(opts?: ConnectOptions): Promise<Result>;
    disconnect(): Promise<Result>;
    sendOrder(order: string, data?: unknown, target?: string): Promise<Result>;
    onOrder(order: string, callback: (payload: any) => void): () => void;
    offOrder(order: string, callback: (payload: any) => void): void;
    getStatus(): Promise<{ connected: boolean; gameState?: GameState | null; currentScene?: string | null } & Record<string, unknown>>;
    requestGameState(): Promise<Result>;
}

declare const clientService: ClientService;
export default clientService;
