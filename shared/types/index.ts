/**
 * Core NVC domain types shared between web and mobile applications
 */

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  createdAt: Date;
  updatedAt: Date;
  preferences: UserPreferences;
  researchConsent?: ResearchConsent;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  language: string;
  notifications: NotificationSettings;
  accessibility: AccessibilitySettings;
}

export interface NotificationSettings {
  sessionReminders: boolean;
  progressUpdates: boolean;
  researchInvitations: boolean;
  pushNotifications: boolean;
}

export interface AccessibilitySettings {
  highContrast: boolean;
  largeText: boolean;
  screenReader: boolean;
  hapticFeedback: boolean;
}

export interface ResearchConsent {
  basicAnalytics: boolean;
  conversationAnalysis: boolean;
  longitudinalStudy: boolean;
  experimentalFeatures: boolean;
  academicResearch: boolean;
  consentDate: Date;
  lastUpdated: Date;
}

export type NVCStepType = 'observation' | 'feeling' | 'need' | 'request';

export interface NVCStep {
  id: string;
  type: NVCStepType;
  title: string;
  description: string;
  userInput?: string;
  aiResponse?: string;
  completed: boolean;
  qualityScore?: number;
  completedAt?: Date;
}

export interface ConversationSession {
  id: string;
  userId: string;
  title: string;
  currentStep: NVCStepType;
  steps: NVCStep[];
  messages: Message[];
  status: SessionStatus;
  createdAt: Date;
  updatedAt: Date;
  completedAt?: Date;
  sessionType: SessionType;
  context?: SessionContext;
}

export type SessionStatus = 'active' | 'paused' | 'completed' | 'abandoned';
export type SessionType = 'personal_practice' | 'conflict_resolution' | 'skill_building' | 'research_study';

export interface SessionContext {
  trigger?: string;
  participants?: string[];
  setting?: string;
  urgency?: 'low' | 'medium' | 'high';
}

export interface Message {
  id: string;
  sessionId: string;
  role: 'user' | 'ai' | 'system';
  content: string;
  timestamp: Date;
  metadata?: MessageMetadata;
}

export interface MessageMetadata {
  aiModel?: string;
  responseTime?: number;
  confidence?: number;
  nvcElements?: NVCElements;
}

export interface NVCElements {
  observations?: string[];
  feelings?: string[];
  needs?: string[];
  requests?: string[];
}

export interface Feeling {
  id: string;
  name: string;
  category: FeelingCategory;
  description: string;
  intensity: 'low' | 'medium' | 'high';
  pleasant: boolean;
  synonyms: string[];
}

export type FeelingCategory = 
  | 'joyful' 
  | 'peaceful' 
  | 'powerful' 
  | 'loving' 
  | 'sad' 
  | 'angry' 
  | 'fearful' 
  | 'confused';

export interface Need {
  id: string;
  name: string;
  category: NeedCategory;
  description: string;
  examples: string[];
  relatedNeeds: string[];
}

export type NeedCategory = 
  | 'autonomy' 
  | 'connection' 
  | 'honesty' 
  | 'play' 
  | 'peace' 
  | 'physical_wellbeing' 
  | 'meaning';

export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: APIError;
  timestamp: Date;
}

export interface APIError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

// Real-time WebSocket message types
export interface WebSocketMessage {
  type: WebSocketMessageType;
  payload: any;
  sessionId?: string;
  timestamp: Date;
}

export type WebSocketMessageType = 
  | 'session_start'
  | 'session_end'
  | 'message_send'
  | 'message_receive'
  | 'step_complete'
  | 'typing_start'
  | 'typing_end'
  | 'error'
  | 'reconnect';

// Research and analytics types
export interface SessionAnalytics {
  sessionId: string;
  userId: string;
  duration: number;
  stepsCompleted: number;
  messagesExchanged: number;
  averageResponseTime: number;
  qualityScores: Record<NVCStepType, number>;
  userSatisfaction?: number;
  platform: 'web' | 'ios' | 'android';
}

export interface ResearchCohort {
  id: string;
  name: string;
  description: string;
  startDate: Date;
  endDate?: Date;
  participantCount: number;
  status: 'recruiting' | 'active' | 'completed';
}

// Form validation types
export interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterData {
  email: string;
  password: string;
  confirmPassword: string;
  firstName: string;
  lastName: string;
  agreeToTerms: boolean;
  researchConsent?: Partial<ResearchConsent>;
}

export interface UpdateProfileData {
  firstName?: string;
  lastName?: string;
  preferences?: Partial<UserPreferences>;
}

// Configuration types
export interface AppConfig {
  apiBaseUrl: string;
  wsUrl: string;
  enableAnalytics: boolean;
  enableVoice: boolean;
  aiModels: AIModelConfig[];
}

export interface AIModelConfig {
  id: string;
  name: string;
  provider: 'openai' | 'anthropic' | 'google';
  enabled: boolean;
  maxTokens: number;
  temperature: number;
}

// Utility types
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;
export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>;
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};