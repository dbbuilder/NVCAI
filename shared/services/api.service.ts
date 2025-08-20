/**
 * API service for NVC AI Facilitator
 * Shared between web and mobile applications
 */
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  APIResponse,
  ConversationSession,
  User,
  LoginCredentials,
  RegisterData,
  UpdateProfileData,
  Feeling,
  Need,
  SessionAnalytics,
  ResearchConsent,
  ResearchCohort,
  Message,
  NVCStep,
  PaginatedResponse
} from '../types';

export class APIService {
  private client: AxiosInstance;
  private baseURL: string;
  private authToken: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL: `${baseURL}/api/v1`,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use((config) => {
      if (this.authToken) {
        config.headers.Authorization = `Bearer ${this.authToken}`;
      }
      return config;
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.handleAuthError();
        }
        return Promise.reject(error);
      }
    );
  }

  setAuthToken(token: string | null): void {
    this.authToken = token;
  }

  private handleAuthError(): void {
    this.authToken = null;
    // Platform-specific auth handling will be implemented in web/mobile
  }

  // Authentication endpoints
  async login(credentials: LoginCredentials): Promise<APIResponse<{ user: User; token: string }>> {
    const response = await this.client.post('/auth/login', credentials);
    return response.data;
  }

  async register(data: RegisterData): Promise<APIResponse<{ user: User; token: string }>> {
    const response = await this.client.post('/auth/register', data);
    return response.data;
  }

  async refreshToken(): Promise<APIResponse<{ token: string }>> {
    const response = await this.client.post('/auth/refresh');
    return response.data;
  }

  async logout(): Promise<APIResponse<void>> {
    const response = await this.client.post('/auth/logout');
    return response.data;
  }

  // User management endpoints
  async getCurrentUser(): Promise<APIResponse<User>> {
    const response = await this.client.get('/users/me');
    return response.data;
  }

  async updateProfile(data: UpdateProfileData): Promise<APIResponse<User>> {
    const response = await this.client.put('/users/me', data);
    return response.data;
  }

  async deleteAccount(): Promise<APIResponse<void>> {
    const response = await this.client.delete('/users/me');
    return response.data;
  }

  // Conversation session endpoints
  async createSession(sessionType: string, context?: any): Promise<APIResponse<ConversationSession>> {
    const response = await this.client.post('/conversations', {
      sessionType,
      context,
    });
    return response.data;
  }

  async getSession(sessionId: string): Promise<APIResponse<ConversationSession>> {
    const response = await this.client.get(`/conversations/${sessionId}`);
    return response.data;
  }

  async getSessions(page = 1, pageSize = 20): Promise<APIResponse<PaginatedResponse<ConversationSession>>> {
    const response = await this.client.get('/conversations', {
      params: { page, pageSize },
    });
    return response.data;
  }

  async updateSession(sessionId: string, updates: Partial<ConversationSession>): Promise<APIResponse<ConversationSession>> {
    const response = await this.client.put(`/conversations/${sessionId}`, updates);
    return response.data;
  }

  async deleteSession(sessionId: string): Promise<APIResponse<void>> {
    const response = await this.client.delete(`/conversations/${sessionId}`);
    return response.data;
  }

  // Message endpoints
  async sendMessage(sessionId: string, content: string): Promise<APIResponse<Message>> {
    const response = await this.client.post(`/conversations/${sessionId}/messages`, {
      content,
    });
    return response.data;
  }

  async getMessages(sessionId: string, page = 1, pageSize = 50): Promise<APIResponse<PaginatedResponse<Message>>> {
    const response = await this.client.get(`/conversations/${sessionId}/messages`, {
      params: { page, pageSize },
    });
    return response.data;
  }

  // NVC step endpoints
  async completeStep(sessionId: string, stepId: string, userInput: string): Promise<APIResponse<NVCStep>> {
    const response = await this.client.post(`/conversations/${sessionId}/steps/${stepId}/complete`, {
      userInput,
    });
    return response.data;
  }

  async getStepGuidance(stepType: string, context?: any): Promise<APIResponse<string>> {
    const response = await this.client.post('/nvc/guidance', {
      stepType,
      context,
    });
    return response.data;
  }

  // NVC resources endpoints
  async getFeelings(): Promise<APIResponse<Feeling[]>> {
    const response = await this.client.get('/nvc/feelings');
    return response.data;
  }

  async getNeeds(): Promise<APIResponse<Need[]>> {
    const response = await this.client.get('/nvc/needs');
    return response.data;
  }

  async getNVCExamples(category?: string): Promise<APIResponse<any[]>> {
    const response = await this.client.get('/nvc/examples', {
      params: { category },
    });
    return response.data;
  }

  // Research endpoints
  async updateResearchConsent(consent: Partial<ResearchConsent>): Promise<APIResponse<ResearchConsent>> {
    const response = await this.client.post('/research/consent', consent);
    return response.data;
  }

  async getResearchCohorts(): Promise<APIResponse<ResearchCohort[]>> {
    const response = await this.client.get('/research/cohorts');
    return response.data;
  }

  async enrollInResearch(cohortId: string, demographics: any): Promise<APIResponse<void>> {
    const response = await this.client.post('/research/enroll', {
      cohortId,
      demographics,
    });
    return response.data;
  }

  async submitSessionAnalytics(analytics: SessionAnalytics): Promise<APIResponse<void>> {
    const response = await this.client.post('/research/session-analytics', analytics);
    return response.data;
  }

  async getABTestAssignment(experimentName: string): Promise<APIResponse<{ variant: string | null }>> {
    const response = await this.client.get(`/research/ab-test/${experimentName}`);
    return response.data;
  }

  // Health and status endpoints
  async healthCheck(): Promise<APIResponse<{ status: string; version: string }>> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

// Singleton instance factory
let apiServiceInstance: APIService | null = null;

export const createAPIService = (baseURL: string): APIService => {
  if (!apiServiceInstance) {
    apiServiceInstance = new APIService(baseURL);
  }
  return apiServiceInstance;
};

export const getAPIService = (): APIService => {
  if (!apiServiceInstance) {
    throw new Error('API Service not initialized. Call createAPIService first.');
  }
  return apiServiceInstance;
};