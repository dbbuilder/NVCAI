/**
 * Main export file for shared NVC AI Facilitator library
 */

// Export all types
export * from '../types';

// Export all services
export * from '../services/api.service';
export * from '../services/websocket.service';

// Export all utilities
export * from '../utils';

// Export all constants
export * from '../constants';

// Re-export commonly used items for convenience
export type {
  User,
  ConversationSession,
  NVCStep,
  Message,
  Feeling,
  Need,
  SessionAnalytics,
  ResearchConsent,
} from '../types';

export {
  NVC_STEPS,
  NVC_STEP_INFO,
  FEELING_CATEGORIES,
  NEED_CATEGORIES,
  SESSION_TYPES,
  SESSION_STATUS,
} from '../constants';