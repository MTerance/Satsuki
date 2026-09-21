import type { Ref } from 'vue';
import type { Socket } from 'socket.io-client';

/** Cibles d'ordre reconnues par le serveur Satsuki */
export declare const OrderTarget: {
    readonly SYSTEM: 'System';
    readonly SCENE: 'Scene';
    readonly QUIZZ: 'Quizz';
};

/** Payload OrderRequest attendu par le serveur Satsuki */
export interface OrderRequestPayload {
    ClientId: string;
    Target: string;
    Order: string;
    JsonData: string;
}

export declare class SocketClient {
    socket: Socket | null;
    isConnected: Ref<boolean>;
    connectionStatus: Ref<string>;

    connect(url?: string | null, options?: object): Socket;
    disconnect(): void;
    emit(event: string, data?: unknown): void;
    on(event: string, callback: (data: any) => void): void;
    off(event: string, callback?: ((data: any) => void) | null): void;

    /** Envoie un ordre au serveur Satsuki au format OrderRequest */
    sendOrder(order: string, data?: unknown, target?: string): OrderRequestPayload;

    joinRoom(roomName: string, userData?: object): void;
    leaveRoom(roomName: string): void;

    startQuiz(quizId: string, userName: string): void;
    submitAnswer(questionId: string, answer: unknown, timeTaken: number): void;
    syncCamera3D(cameraData: { position: unknown; rotation: unknown }): void;
    loadModel3D(modelPath: string, modelData: unknown): void;

    getConnectionStatus(): { isConnected: boolean; status: string; socketId: string | null };
    getConnectionStats(): object | null;
    setServerUrl(url: string): void;
}

declare const socketClient: SocketClient;
export default socketClient;
