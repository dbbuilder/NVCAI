/**
 * Shared utility functions for NVC AI Facilitator
 * Used across web and mobile applications
 */

/**
 * Format a date to a human-readable string
 */
export const formatDate = (date: Date, format: 'short' | 'long' | 'relative' = 'short'): string => {
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMinutes = Math.floor(diffMs / (1000 * 60));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (format === 'relative') {
    if (diffMinutes < 1) return 'Just now';
    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  }

  if (format === 'short') {
    return date.toLocaleDateString();
  }

  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

/**
 * Format session duration in minutes and seconds
 */
export const formatDuration = (durationMs: number): string => {
  const minutes = Math.floor(durationMs / (1000 * 60));
  const seconds = Math.floor((durationMs % (1000 * 60)) / 1000);
  
  if (minutes > 0) {
    return `${minutes}m ${seconds}s`;
  }
  return `${seconds}s`;
};

/**
 * Validate email format
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate password strength
 */
export const validatePassword = (password: string): { isValid: boolean; errors: string[] } => {
  const errors: string[] = [];
  
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long');
  }
  
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }
  
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }
  
  if (!/\d/.test(password)) {
    errors.push('Password must contain at least one number');
  }
  
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('Password must contain at least one special character');
  }
  
  return {
    isValid: errors.length === 0,
    errors,
  };
};

/**
 * Generate a random session ID
 */
export const generateSessionId = (): string => {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * Debounce function for performance optimization
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout | null = null;
  
  return (...args: Parameters<T>) => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    
    timeoutId = setTimeout(() => {
      func(...args);
    }, wait);
  };
};

/**
 * Throttle function for performance optimization
 */
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean = false;
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
};

/**
 * Deep clone an object
 */
export const deepClone = <T>(obj: T): T => {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  
  if (obj instanceof Date) {
    return new Date(obj.getTime()) as unknown as T;
  }
  
  if (obj instanceof Array) {
    return obj.map(item => deepClone(item)) as unknown as T;
  }
  
  if (typeof obj === 'object') {
    const copy = {} as T;
    Object.keys(obj).forEach(key => {
      (copy as any)[key] = deepClone((obj as any)[key]);
    });
    return copy;
  }
  
  return obj;
};

/**
 * Calculate quality score for NVC responses
 */
export const calculateNVCQuality = (
  userInput: string,
  stepType: 'observation' | 'feeling' | 'need' | 'request'
): number => {
  const input = userInput.toLowerCase().trim();
  
  if (!input) return 0;
  
  let score = 50; // Base score
  
  switch (stepType) {
    case 'observation':
      // Check for judgmental language
      const judgmentalWords = ['always', 'never', 'should', 'must', 'wrong', 'bad', 'stupid'];
      const hasJudgment = judgmentalWords.some(word => input.includes(word));
      if (hasJudgment) score -= 20;
      
      // Check for factual language
      const factualIndicators = ['when', 'i saw', 'i heard', 'i noticed'];
      const hasFactual = factualIndicators.some(phrase => input.includes(phrase));
      if (hasFactual) score += 20;
      
      break;
      
    case 'feeling':
      // Check for actual feeling words vs thoughts
      const feelingWords = ['happy', 'sad', 'angry', 'frustrated', 'excited', 'nervous', 'peaceful'];
      const hasFeelingWord = feelingWords.some(word => input.includes(word));
      if (hasFeelingWord) score += 30;
      
      // Penalize for "I feel that" (thought, not feeling)
      if (input.includes('i feel that') || input.includes('i feel like')) score -= 15;
      
      break;
      
    case 'need':
      // Check for universal needs language
      const needWords = ['understanding', 'respect', 'connection', 'autonomy', 'safety', 'belonging'];
      const hasNeedWord = needWords.some(word => input.includes(word));
      if (hasNeedWord) score += 25;
      
      // Check for strategies disguised as needs
      if (input.includes('you to') || input.includes('them to')) score -= 20;
      
      break;
      
    case 'request':
      // Check for specific, doable requests
      if (input.includes('would you') || input.includes('could you')) score += 20;
      if (input.includes('please')) score += 10;
      
      // Penalize demands
      if (input.includes('must') || input.includes('have to')) score -= 25;
      
      break;
  }
  
  // Length considerations
  if (input.length < 10) score -= 10;
  if (input.length > 200) score -= 5;
  
  return Math.max(0, Math.min(100, score));
};

/**
 * Extract emotions from text using simple keyword matching
 */
export const extractEmotions = (text: string): string[] => {
  const emotions = [
    'happy', 'joy', 'excited', 'grateful', 'peaceful', 'content',
    'sad', 'disappointed', 'hurt', 'lonely', 'grief',
    'angry', 'frustrated', 'irritated', 'annoyed', 'rage',
    'fearful', 'worried', 'anxious', 'nervous', 'scared',
    'confused', 'overwhelmed', 'uncertain', 'lost'
  ];
  
  const lowerText = text.toLowerCase();
  return emotions.filter(emotion => lowerText.includes(emotion));
};

/**
 * Sanitize user input for security
 */
export const sanitizeInput = (input: string): string => {
  return input
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+\s*=\s*["'][^"']*["']/gi, '')
    .trim();
};

/**
 * Generate a user-friendly error message
 */
export const formatErrorMessage = (error: any): string => {
  if (typeof error === 'string') {
    return error;
  }
  
  if (error?.response?.data?.message) {
    return error.response.data.message;
  }
  
  if (error?.message) {
    return error.message;
  }
  
  return 'An unexpected error occurred. Please try again.';
};

/**
 * Check if running on mobile platform
 */
export const isMobile = (): boolean => {
  // This will be implemented differently in web vs React Native
  if (typeof navigator !== 'undefined') {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  }
  return false;
};

/**
 * Storage utility functions (will be implemented differently for web vs mobile)
 */
export interface StorageUtils {
  setItem(key: string, value: string): Promise<void>;
  getItem(key: string): Promise<string | null>;
  removeItem(key: string): Promise<void>;
  clear(): Promise<void>;
}

/**
 * Create storage utils factory (platform-specific implementation)
 */
export const createStorageUtils = (): StorageUtils => {
  // This will be overridden in platform-specific implementations
  throw new Error('Storage utils must be implemented for specific platform');
};

/**
 * Color utilities for consistent theming
 */
export const colors = {
  primary: {
    50: '#f0f9ff',
    100: '#e0f2fe',
    500: '#0ea5e9',
    600: '#0284c7',
    700: '#0369a1',
  },
  success: {
    50: '#f0fdf4',
    500: '#22c55e',
    600: '#16a34a',
  },
  warning: {
    50: '#fffbeb',
    500: '#f59e0b',
    600: '#d97706',
  },
  error: {
    50: '#fef2f2',
    500: '#ef4444',
    600: '#dc2626',
  },
  neutral: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    500: '#6b7280',
    700: '#374151',
    900: '#111827',
  },
} as const;

/**
 * Animation duration constants
 */
export const animations = {
  fast: 150,
  normal: 300,
  slow: 500,
} as const;

/**
 * Breakpoint constants for responsive design
 */
export const breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
} as const;