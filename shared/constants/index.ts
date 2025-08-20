/**
 * Shared constants for NVC AI Facilitator
 * Used across web and mobile applications
 */

// API Configuration
export const API_CONFIG = {
  VERSION: 'v1',
  TIMEOUT: 30000,
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000,
} as const;

// WebSocket Configuration
export const WS_CONFIG = {
  RECONNECTION_ATTEMPTS: 5,
  RECONNECTION_DELAY: 1000,
  HEARTBEAT_INTERVAL: 30000,
  PING_TIMEOUT: 5000,
} as const;

// Session Configuration
export const SESSION_CONFIG = {
  MAX_DURATION_HOURS: 4,
  AUTO_SAVE_INTERVAL: 30000, // 30 seconds
  IDLE_TIMEOUT: 1800000, // 30 minutes
  MAX_MESSAGES: 1000,
} as const;

// NVC Step Types
export const NVC_STEPS = {
  OBSERVATION: 'observation',
  FEELING: 'feeling', 
  NEED: 'need',
  REQUEST: 'request',
} as const;

// NVC Step Titles and Descriptions
export const NVC_STEP_INFO = {
  [NVC_STEPS.OBSERVATION]: {
    title: 'Observation',
    description: 'Describe what you observed without evaluation or interpretation',
    prompt: 'What did you see or hear that triggered your reaction?',
    placeholder: 'When I saw/heard...',
  },
  [NVC_STEPS.FEELING]: {
    title: 'Feeling',
    description: 'Express how you feel about what you observed',
    prompt: 'How are you feeling about this situation?',
    placeholder: 'I feel...',
  },
  [NVC_STEPS.NEED]: {
    title: 'Need',
    description: 'Identify the underlying need that creates your feelings',
    prompt: 'What need of yours is not being met?',
    placeholder: 'I need...',
  },
  [NVC_STEPS.REQUEST]: {
    title: 'Request',
    description: 'Make a specific, doable request to meet your need',
    prompt: 'What specific action would you like to request?',
    placeholder: 'Would you be willing to...',
  },
} as const;

// Feeling Categories
export const FEELING_CATEGORIES = {
  JOYFUL: 'joyful',
  PEACEFUL: 'peaceful',
  POWERFUL: 'powerful',
  LOVING: 'loving',
  SAD: 'sad',
  ANGRY: 'angry',
  FEARFUL: 'fearful',
  CONFUSED: 'confused',
} as const;

// Need Categories
export const NEED_CATEGORIES = {
  AUTONOMY: 'autonomy',
  CONNECTION: 'connection',
  HONESTY: 'honesty',
  PLAY: 'play',
  PEACE: 'peace',
  PHYSICAL_WELLBEING: 'physical_wellbeing',
  MEANING: 'meaning',
} as const;

// Common Feelings by Category
export const FEELINGS_BY_CATEGORY = {
  [FEELING_CATEGORIES.JOYFUL]: [
    'happy', 'excited', 'grateful', 'delighted', 'joyful', 'elated',
    'enthusiastic', 'optimistic', 'hopeful', 'cheerful', 'content'
  ],
  [FEELING_CATEGORIES.PEACEFUL]: [
    'calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'centered',
    'balanced', 'secure', 'comfortable', 'satisfied', 'fulfilled'
  ],
  [FEELING_CATEGORIES.POWERFUL]: [
    'confident', 'empowered', 'strong', 'capable', 'determined', 'energetic',
    'motivated', 'inspired', 'courageous', 'proud', 'accomplished'
  ],
  [FEELING_CATEGORIES.LOVING]: [
    'loving', 'affectionate', 'tender', 'caring', 'compassionate', 'warm',
    'connected', 'close', 'intimate', 'appreciative', 'grateful'
  ],
  [FEELING_CATEGORIES.SAD]: [
    'sad', 'disappointed', 'hurt', 'lonely', 'dejected', 'discouraged',
    'heavy', 'melancholy', 'sorrowful', 'grief', 'heartbroken'
  ],
  [FEELING_CATEGORIES.ANGRY]: [
    'angry', 'frustrated', 'irritated', 'annoyed', 'furious', 'outraged',
    'resentful', 'indignant', 'livid', 'bitter', 'hostile'
  ],
  [FEELING_CATEGORIES.FEARFUL]: [
    'afraid', 'scared', 'worried', 'anxious', 'nervous', 'terrified',
    'panicked', 'alarmed', 'concerned', 'apprehensive', 'uneasy'
  ],
  [FEELING_CATEGORIES.CONFUSED]: [
    'confused', 'puzzled', 'perplexed', 'bewildered', 'uncertain', 'lost',
    'overwhelmed', 'disoriented', 'mixed up', 'conflicted', 'torn'
  ],
} as const;

// Universal Human Needs by Category
export const NEEDS_BY_CATEGORY = {
  [NEED_CATEGORIES.AUTONOMY]: [
    'choice', 'freedom', 'independence', 'space', 'spontaneity',
    'self-determination', 'autonomy', 'empowerment', 'self-expression'
  ],
  [NEED_CATEGORIES.CONNECTION]: [
    'acceptance', 'affection', 'appreciation', 'belonging', 'cooperation',
    'communication', 'closeness', 'community', 'companionship', 'compassion',
    'consideration', 'consistency', 'empathy', 'inclusion', 'intimacy',
    'love', 'mutuality', 'nurturing', 'respect', 'safety', 'security',
    'stability', 'support', 'to know and be known', 'to see and be seen',
    'to understand and be understood', 'trust', 'warmth'
  ],
  [NEED_CATEGORIES.HONESTY]: [
    'authenticity', 'integrity', 'presence', 'transparency', 'honesty',
    'genuineness', 'sincerity', 'truth', 'openness', 'directness'
  ],
  [NEED_CATEGORIES.PLAY]: [
    'joy', 'humor', 'play', 'fun', 'recreation', 'relaxation',
    'spontaneity', 'adventure', 'celebration', 'creativity', 'discovery'
  ],
  [NEED_CATEGORIES.PEACE]: [
    'beauty', 'communion', 'ease', 'equality', 'harmony', 'inspiration',
    'order', 'peace', 'balance', 'calm', 'tranquility', 'serenity'
  ],
  [NEED_CATEGORIES.PHYSICAL_WELLBEING]: [
    'air', 'food', 'movement', 'rest', 'sexual expression', 'safety',
    'shelter', 'touch', 'water', 'health', 'exercise', 'sleep'
  ],
  [NEED_CATEGORIES.MEANING]: [
    'awareness', 'celebration of life', 'challenge', 'clarity', 'competence',
    'consciousness', 'contribution', 'creativity', 'discovery', 'efficacy',
    'effectiveness', 'growth', 'hope', 'learning', 'mourning', 'participation',
    'purpose', 'self-expression', 'stimulation', 'to matter', 'understanding'
  ],
} as const;

// Session Types
export const SESSION_TYPES = {
  PERSONAL_PRACTICE: 'personal_practice',
  CONFLICT_RESOLUTION: 'conflict_resolution',
  SKILL_BUILDING: 'skill_building',
  RESEARCH_STUDY: 'research_study',
} as const;

// Session Status
export const SESSION_STATUS = {
  ACTIVE: 'active',
  PAUSED: 'paused',
  COMPLETED: 'completed',
  ABANDONED: 'abandoned',
} as const;

// Message Roles
export const MESSAGE_ROLES = {
  USER: 'user',
  AI: 'ai',
  SYSTEM: 'system',
} as const;

// WebSocket Message Types
export const WS_MESSAGE_TYPES = {
  SESSION_START: 'session_start',
  SESSION_END: 'session_end',
  MESSAGE_SEND: 'message_send',
  MESSAGE_RECEIVE: 'message_receive',
  STEP_COMPLETE: 'step_complete',
  TYPING_START: 'typing_start',
  TYPING_END: 'typing_end',
  ERROR: 'error',
  RECONNECT: 'reconnect',
} as const;

// AI Models
export const AI_MODELS = {
  OPENAI_GPT4: 'gpt-4',
  OPENAI_GPT35: 'gpt-3.5-turbo',
  ANTHROPIC_CLAUDE: 'claude-3-sonnet',
  GOOGLE_GEMINI: 'gemini-pro',
} as const;

// Research Consent Types
export const RESEARCH_CONSENT_TYPES = {
  BASIC_ANALYTICS: 'basic_analytics',
  CONVERSATION_ANALYSIS: 'conversation_analysis',
  LONGITUDINAL_STUDY: 'longitudinal_study',
  EXPERIMENTAL_FEATURES: 'experimental_features',
  ACADEMIC_RESEARCH: 'academic_research',
} as const;

// Quality Score Thresholds
export const QUALITY_THRESHOLDS = {
  EXCELLENT: 90,
  GOOD: 70,
  FAIR: 50,
  POOR: 30,
} as const;

// File Upload Limits
export const UPLOAD_LIMITS = {
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_AUDIO_TYPES: ['audio/mp3', 'audio/wav', 'audio/m4a'],
  ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/gif'],
} as const;

// Notification Types
export const NOTIFICATION_TYPES = {
  SESSION_REMINDER: 'session_reminder',
  PROGRESS_UPDATE: 'progress_update',
  RESEARCH_INVITATION: 'research_invitation',
  SYSTEM_UPDATE: 'system_update',
} as const;

// Error Codes
export const ERROR_CODES = {
  AUTHENTICATION_FAILED: 'AUTH_FAILED',
  INVALID_SESSION: 'INVALID_SESSION',
  RATE_LIMIT_EXCEEDED: 'RATE_LIMIT',
  AI_SERVICE_UNAVAILABLE: 'AI_UNAVAILABLE',
  NETWORK_ERROR: 'NETWORK_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  PERMISSION_DENIED: 'PERMISSION_DENIED',
} as const;

// Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_PREFERENCES: 'user_preferences',
  RESEARCH_CONSENT: 'research_consent',
  CACHED_SESSIONS: 'cached_sessions',
  OFFLINE_MESSAGES: 'offline_messages',
} as const;

// App Configuration
export const APP_CONFIG = {
  NAME: 'NVC AI Facilitator',
  VERSION: '1.0.0',
  SUPPORT_EMAIL: 'support@nvc-ai-facilitator.com',
  PRIVACY_URL: 'https://nvc-ai-facilitator.com/privacy',
  TERMS_URL: 'https://nvc-ai-facilitator.com/terms',
} as const;

// Development Environment
export const ENV = {
  DEVELOPMENT: 'development',
  STAGING: 'staging',
  PRODUCTION: 'production',
} as const;

// Platform Types
export const PLATFORMS = {
  WEB: 'web',
  IOS: 'ios',
  ANDROID: 'android',
} as const;