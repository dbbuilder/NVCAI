/**
 * WebSocket service for real-time communication
 * Shared between web and mobile applications
 */
import { io, Socket } from 'socket.io-client';
import { WebSocketMessage, WebSocketMessageType, ConversationSession } from '../types';

export interface WebSocketConfig {
  url: string;
  autoConnect?: boolean;
  reconnectionAttempts?: number;
  reconnectionDelay?: number;
}

export class WebSocketService {
  private socket: Socket | null = null;
  private config: WebSocketConfig;
  private listeners: Map<string, Function[]> = new Map();
  private isConnected = false;
  private currentSessionId: string | null = null;

  constructor(config: WebSocketConfig) {
    this.config = {
      autoConnect: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
      ...config,
    };
  }

  connect(authToken: string): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.socket = io(this.config.url, {
          auth: {
            token: authToken,
          },
          autoConnect: this.config.autoConnect,
          reconnectionAttempts: this.config.reconnectionAttempts,
          reconnectionDelay: this.config.reconnectionDelay,
        });

        this.socket.on('connect', () => {
          this.isConnected = true;
          this.emit('connection_status', { connected: true });
          resolve();
        });

        this.socket.on('disconnect', (reason) => {
          this.isConnected = false;
          this.emit('connection_status', { connected: false, reason });
        });

        this.socket.on('connect_error', (error) => {
          this.isConnected = false;
          this.emit('connection_error', error);
          reject(error);
        });

        this.socket.on('message', (data: WebSocketMessage) => {
          this.handleMessage(data);
        });

        // NVC-specific event handlers
        this.socket.on('ai_response', (data) => {
          this.emit('ai_response', data);
        });

        this.socket.on('typing_indicator', (data) => {
          this.emit('typing_indicator', data);
        });

        this.socket.on('session_update', (data) => {
          this.emit('session_update', data);
        });

        this.socket.on('step_guidance', (data) => {
          this.emit('step_guidance', data);
        });

      } catch (error) {
        reject(error);
      }
    });
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
      this.currentSessionId = null;
    }
  }

  private handleMessage(message: WebSocketMessage): void {
    this.emit(message.type, message.payload);
  }

  // Session management
  joinSession(sessionId: string): void {
    if (this.socket && this.isConnected) {
      this.currentSessionId = sessionId;
      this.socket.emit('join_session', { sessionId });
    }
  }

  leaveSession(): void {
    if (this.socket && this.isConnected && this.currentSessionId) {
      this.socket.emit('leave_session', { sessionId: this.currentSessionId });
      this.currentSessionId = null;
    }
  }

  // Message sending
  sendMessage(content: string, sessionId?: string): void {
    const targetSession = sessionId || this.currentSessionId;
    if (this.socket && this.isConnected && targetSession) {
      this.socket.emit('send_message', {
        sessionId: targetSession,
        content,
        timestamp: new Date(),
      });
    }
  }

  // NVC step interactions
  requestStepGuidance(stepType: string, context?: any): void {
    if (this.socket && this.isConnected && this.currentSessionId) {
      this.socket.emit('request_guidance', {
        sessionId: this.currentSessionId,
        stepType,
        context,
      });
    }
  }

  completeStep(stepId: string, userInput: string): void {
    if (this.socket && this.isConnected && this.currentSessionId) {
      this.socket.emit('complete_step', {
        sessionId: this.currentSessionId,
        stepId,
        userInput,
      });
    }
  }

  // Typing indicators
  startTyping(): void {
    if (this.socket && this.isConnected && this.currentSessionId) {
      this.socket.emit('typing_start', {
        sessionId: this.currentSessionId,
      });
    }
  }

  stopTyping(): void {
    if (this.socket && this.isConnected && this.currentSessionId) {
      this.socket.emit('typing_end', {
        sessionId: this.currentSessionId,
      });
    }
  }

  // Event handling
  on(event: string, callback: Function): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
  }

  off(event: string, callback?: Function): void {
    if (callback) {
      const eventListeners = this.listeners.get(event);
      if (eventListeners) {
        const index = eventListeners.indexOf(callback);
        if (index !== -1) {
          eventListeners.splice(index, 1);
        }
      }
    } else {
      this.listeners.delete(event);
    }
  }

  private emit(event: string, data: any): void {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in WebSocket event handler for ${event}:`, error);
        }
      });
    }
  }

  // Status getters
  get connected(): boolean {
    return this.isConnected;
  }

  get sessionId(): string | null {
    return this.currentSessionId;
  }

  // Utility methods
  ping(): Promise<number> {
    return new Promise((resolve) => {
      if (this.socket && this.isConnected) {
        const startTime = Date.now();
        this.socket.emit('ping', startTime, () => {
          resolve(Date.now() - startTime);
        });
      } else {
        resolve(-1);
      }
    });
  }
}

// Singleton instance factory
let webSocketServiceInstance: WebSocketService | null = null;

export const createWebSocketService = (config: WebSocketConfig): WebSocketService => {
  if (!webSocketServiceInstance) {
    webSocketServiceInstance = new WebSocketService(config);
  }
  return webSocketServiceInstance;
};

export const getWebSocketService = (): WebSocketService => {
  if (!webSocketServiceInstance) {
    throw new Error('WebSocket Service not initialized. Call createWebSocketService first.');
  }
  return webSocketServiceInstance;
};