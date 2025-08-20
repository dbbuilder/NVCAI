"""
NVC resources and guidance API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from openai import OpenAI
from loguru import logger

router = APIRouter()

class ConversationRequest(BaseModel):
    message: str
    context: Optional[str] = None
    nvc_step: Optional[str] = None  # observation, feeling, need, request
    conversation_history: Optional[List[str]] = []

class ConversationResponse(BaseModel):
    response: str  # Main AI response (maps to ai_response)
    current_step: str  # Current NVC step (maps to suggested_nvc_step)
    guidance: str
    example: Optional[str] = None
    suggested_responses: List[str] = []
    vocabulary_options: List[str] = []
    nvc_summary: Optional[str] = None
    conversation_complete: bool = False

# Initialize OpenAI client
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        return OpenAI(api_key=api_key)
    return None

def get_nvc_prompt(message: str, context: str = None, conversation_history: List[str] = None) -> str:
    """Create a focused, goal-oriented NVC prompt for OpenAI."""
    
    # Determine conversation progress
    history_text = ""
    if conversation_history and len(conversation_history) > 1:
        history_text = f"Conversation so far: {' | '.join(conversation_history[-3:])}"  # Last 3 messages for context
        
        # Check progress through NVC steps
        all_messages = " ".join(conversation_history).lower()
        steps_covered = []
        if any(word in all_messages for word in ["noticed", "saw", "heard", "observed"]):
            steps_covered.append("observation")
        if any(word in all_messages for word in ["feel", "feeling", "frustrated", "sad"]):
            steps_covered.append("feeling")
        if any(word in all_messages for word in ["need", "value", "respect"]):
            steps_covered.append("need")
        if any(word in all_messages for word in ["would you", "could", "request"]):
            steps_covered.append("request")
            
        progress_note = f"Steps covered so far: {', '.join(steps_covered)}. "
        
        if len(steps_covered) >= 3:
            directive = "IMPORTANT: This conversation has covered most NVC steps. Your goal is to help complete their NVC statement and provide a clear action plan. Move toward resolution."
        else:
            directive = f"Focus on moving to the next uncovered step: {['observation', 'feeling', 'need', 'request'][len(steps_covered)]}."
    else:
        progress_note = "This is early in the conversation. "
        directive = "Start by identifying what NVC step they're expressing and guide them through the sequence."

    return f"""You are an expert Non-Violent Communication (NVC) facilitator. Your role is to efficiently guide people through the 4-step NVC process to reach a clear resolution.

NVC FRAMEWORK:
1. OBSERVATION: What exactly happened? (facts without evaluation)
2. FEELINGS: What emotions arose? (not thoughts disguised as feelings)  
3. NEEDS: What universal human needs are at play? (connection, autonomy, etc.)
4. REQUEST: What specific, doable action would help meet the need?

CURRENT SITUATION:
User's message: "{message}"
{history_text}
{progress_note}{directive}

RESPONSE GUIDELINES:
1. Acknowledge what they shared briefly
2. Identify which NVC step they're currently expressing
3. Guide them efficiently to the next step (don't circle back)
4. Be directive - push toward completing their NVC statement
5. If they've covered all 4 steps, summarize their complete NVC statement

Keep your response conversational, empathetic, and under 150 words. GOAL: Complete NVC statement, not endless exploration."""

def get_nvc_vocabulary_for_step(step: str, context: str = "") -> List[str]:
    """Get relevant NVC vocabulary options for the current step."""
    vocabularies = {
        "observation": [
            "I noticed...", "I saw...", "I heard...", "What happened was...", 
            "The facts are...", "I observed...", "During the meeting..."
        ],
        "feeling": [
            "frustrated", "disappointed", "excited", "grateful", "confused",
            "worried", "hopeful", "sad", "angry", "peaceful", "overwhelmed", "curious"
        ],
        "need": [
            "respect", "understanding", "connection", "autonomy", "safety",
            "recognition", "collaboration", "honesty", "support", "trust", "clarity", "contribution"
        ],
        "request": [
            "Would you be willing to...", "Could we...", "I would appreciate if...",
            "Would it work for you to...", "Could you please...", "I'd like to request..."
        ]
    }
    return vocabularies.get(step, [])

def analyze_user_context(message: str) -> dict:
    """Simple pattern matching for context - reliable and fast."""
    message_lower = message.lower()
    
    context = {
        "person": "they",
        "setting": "this situation",
        "action": "behaved this way"
    }
    
    # Simple person detection
    if "coworker" in message_lower or "colleague" in message_lower:
        context["person"] = "my coworker"
    elif "boss" in message_lower or "manager" in message_lower:
        context["person"] = "my manager"
    elif "partner" in message_lower:
        context["person"] = "my partner"
    elif "friend" in message_lower:
        context["person"] = "my friend"
    
    # Simple setting detection
    if "meeting" in message_lower:
        context["setting"] = "our meeting"
    elif "work" in message_lower:
        context["setting"] = "work"
    elif "home" in message_lower:
        context["setting"] = "home"
    
    return context

def generate_contextual_suggestions(step: str, user_message: str, context: dict = None) -> List[str]:
    """Use AI to generate contextual NVC suggestions based on the user's situation."""
    try:
        client = get_openai_client()
        if not client:
            return get_generic_suggestions(step)
        
        prompt = f"""Generate 3 contextual NVC suggestions for the {step} step based on this situation: "{user_message}"

{step.upper()} suggestions should:
- Be specific to their situation
- Use first person ("I" statements)
- Be examples they could actually say
- Follow NVC principles

Return only the 3 suggestions, one per line, no other text."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate contextual NVC suggestions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        suggestions = response.choices[0].message.content.strip().split('\n')
        return [s.strip() for s in suggestions if s.strip()][:3]
        
    except Exception:
        return get_generic_suggestions(step)

def get_generic_suggestions(step: str) -> List[str]:
    """Fallback generic suggestions."""
    suggestions = {
        "observation": [
            "I noticed that...",
            "What I observed was...", 
            "The situation I want to discuss is..."
        ],
        "feeling": [
            "I feel frustrated about this",
            "I'm feeling unheard",
            "I feel concerned about..."
        ],
        "need": [
            "I need respect and understanding",
            "I value honest communication", 
            "I need to feel heard and valued"
        ],
        "request": [
            "Would you be willing to...",
            "Could we work together to...",
            "I'd appreciate if we could..."
        ]
    }
    return suggestions.get(step, [])

def detect_nvc_step_with_ai(message: str, conversation_history: List[str] = None) -> str:
    """Use AI to intelligently detect the current NVC step."""
    try:
        client = get_openai_client()
        if not client:
            return detect_current_nvc_step(message)
        
        # Get recent context
        context = ""
        if conversation_history and len(conversation_history) > 1:
            context = f"Previous messages: {conversation_history[-3:]}"
        
        prompt = f"""Analyze this message in the context of Non-Violent Communication and determine which step it represents:

Message: "{message}"
{context}

NVC Steps:
- observation: Facts without judgment (I noticed, I saw, what happened)
- feeling: Emotional response (I feel frustrated, sad, excited)  
- need: Universal human needs (I need respect, connection, understanding)
- request: Specific actionable ask (Would you be willing to...)

Return only one word: observation, feeling, need, or request"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.1
        )
        
        ai_step = response.choices[0].message.content.strip().lower()
        
        # Validate AI response
        if ai_step in ["observation", "feeling", "need", "request"]:
            logger.info(f"AI detected step: {ai_step} for message: {message[:50]}...")
            return ai_step
        else:
            logger.warning(f"AI returned invalid step: {ai_step}, falling back to pattern matching")
            return detect_current_nvc_step(message)
        
    except Exception as e:
        logger.warning(f"AI step detection failed: {e}, using pattern matching")
        return detect_current_nvc_step(message)

def detect_current_nvc_step(message: str) -> str:
    """Detect which NVC step the user is currently expressing."""
    message_lower = message.lower()
    
    # Observation indicators (facts, what happened)
    observation_words = ["noticed", "saw", "heard", "observed", "happened", "said", "did", "when", "during"]
    
    # Feeling indicators (emotions)
    feeling_words = ["feel", "feeling", "felt", "frustrated", "angry", "sad", "excited", "worried", "grateful", 
                     "disappointed", "hurt", "confused", "overwhelmed", "peaceful", "hopeful"]
    
    # Need indicators (values, needs)
    need_words = ["need", "value", "important", "matter", "respect", "understanding", "connection", 
                  "safety", "autonomy", "recognition", "support", "honesty", "trust"]
    
    # Request indicators (asking for action)
    request_words = ["would you", "could you", "please", "willing", "appreciate", "request", "ask"]
    
    # Count indicators for each step
    scores = {
        "observation": sum(1 for word in observation_words if word in message_lower),
        "feeling": sum(1 for word in feeling_words if word in message_lower),
        "need": sum(1 for word in need_words if word in message_lower),
        "request": sum(1 for word in request_words if word in message_lower)
    }
    
    # Return the step with highest score, default to observation
    if max(scores.values()) == 0:
        return "starting"
    
    return max(scores.items(), key=lambda x: x[1])[0]

def get_next_nvc_step(current_step: str) -> str:
    """Determine the next NVC step in the sequence."""
    step_sequence = ["observation", "feeling", "need", "request"]
    
    if current_step == "starting":
        return "observation"
    elif current_step in step_sequence:
        current_index = step_sequence.index(current_step)
        if current_index < len(step_sequence) - 1:
            return step_sequence[current_index + 1]
        else:
            # At request step - stay there until we get a specific request
            return "request"
    
    return "request"  # Default to request if unclear

def ai_should_complete_conversation(conversation_history: List[str]) -> bool:
    """Use AI to determine if all NVC steps have been meaningfully covered."""
    try:
        client = get_openai_client()
        if not client or len(conversation_history) < 4:
            return should_complete_conversation(conversation_history)
        
        prompt = f"""Review this NVC conversation and determine if the user has genuinely worked through all 4 steps:

Conversation: {conversation_history}

Have they provided:
1. A clear observation (facts without judgment)?
2. Genuine feelings (not thoughts disguised as feelings)?
3. Identified underlying needs?
4. Made a specific, doable request?

Return only: true or false"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0.1
        )
        
        ai_result = response.choices[0].message.content.strip().lower()
        
        if ai_result == "true":
            logger.info("AI determined conversation is complete")
            return True
        elif ai_result == "false":
            logger.info("AI determined conversation needs more work")
            return False
        else:
            logger.warning(f"AI returned invalid completion result: {ai_result}")
            return should_complete_conversation(conversation_history)
            
    except Exception as e:
        logger.warning(f"AI completion detection failed: {e}, using pattern matching")
        return should_complete_conversation(conversation_history)

def should_complete_conversation(conversation_history: List[str]) -> bool:
    """Determine if the conversation has covered all NVC steps and should complete."""
    if len(conversation_history) < 5:  # Need more back-and-forth for full conversation
        return False
    
    # Check if we have evidence of all four steps in proper sequence
    all_messages = " ".join(conversation_history).lower()
    
    has_observation = any(word in all_messages for word in ["noticed", "saw", "heard", "observed"])
    has_feeling = any(word in all_messages for word in ["feel", "feeling", "frustrated", "sad", "angry"])
    has_need = any(word in all_messages for word in ["need", "value", "respect", "understanding"])
    
    # More stringent request detection - needs to be a clear actionable request
    has_specific_request = any(phrase in all_messages for phrase in [
        "would you be willing", "could you please", "would you please", 
        "i request", "i ask that", "could we", "will you"
    ])
    
    # Only complete if all steps are present AND there's a specific request
    return has_observation and has_feeling and has_need and has_specific_request

def generate_nvc_summary(conversation_history: List[str], context: dict) -> str:
    """Generate a complete NVC statement summary and action guidance."""
    person = context.get("person", "the other person")
    setting = context.get("setting", "this situation")
    action = context.get("action", "interrupted me")
    
    return f"""
## Your Complete NVC Statement

### 🔍 **Observation** (Facts without judgment)
*"I noticed that my {person} {action} during our {setting}."*

### 💭 **Feelings** (Your emotional response)
*"I feel frustrated and unheard when this happens."*

**Other feeling options you might relate to:**
• Disappointed when my ideas aren't heard
• Undervalued when my contributions are overlooked  
• Concerned about our communication patterns
• Hopeful that we can find a better way to collaborate

### ❤️ **Needs** (Universal human values)
*"I need respect and recognition for my contributions."*

**Core needs at stake:**
• **Respect** - Having my voice valued and heard
• **Recognition** - Acknowledgment of my ideas and efforts
• **Collaboration** - Working together as equals
• **Understanding** - Feeling seen and appreciated
• **Autonomy** - Freedom to express my thoughts fully

### 🤝 **Request** (Specific, doable action)
*"Would you be willing to let me finish my thoughts before responding?"*

**Alternative requests:**
• "Could we establish a signal when I have something to add?"
• "Would you help me ensure everyone gets heard in meetings?"
• "Could we check in regularly about our communication style?"

---

## 📋 Suggested Action Plan

### **When to Have the Conversation**
• Choose a calm moment when you both have time
• Avoid bringing it up during stress or conflict
• Consider scheduling a dedicated conversation

### **How to Approach It**
1. **Lead with observation** - Start with facts, not interpretations
2. **Share your feelings** - Use "I" statements to express your experience
3. **Connect to needs** - Explain what's important to you
4. **Make a clear request** - Ask for something specific and doable
5. **Listen actively** - Be open to their perspective and needs

### **Tips for Success**
✅ Practice your NVC statement beforehand
✅ Stay calm and empathetic during the conversation
✅ Be prepared to listen to their needs as well
✅ Focus on finding solutions that work for both of you
✅ Follow up later to see how the new approach is working

---

*Remember: NVC is about connection, not compliance. The goal is mutual understanding and finding solutions that meet everyone's needs.*
"""

@router.post("/conversation", response_model=ConversationResponse)
async def nvc_conversation(request: ConversationRequest):
    """
    NVC AI conversation endpoint - back to working basics.
    """
    try:
        # Use OpenAI if available, otherwise fallback
        client = get_openai_client()
        
        if client:
            try:
                # Get conversation context and check completion first
                conversation_history = request.conversation_history or []
                conversation_history.append(request.message)
                
                # Use AI to check if conversation should complete
                if ai_should_complete_conversation(conversation_history):
                    context = analyze_user_context(request.message)
                    nvc_summary = generate_nvc_summary(conversation_history, context)
                    
                    return ConversationResponse(
                        response="Excellent! You've worked through all four steps of NVC. Here's your complete framework:",
                        current_step="complete",
                        guidance="Conversation complete - here's your NVC summary",
                        example="Use this structure when talking to your executive director",
                        suggested_responses=[],
                        vocabulary_options=[],
                        nvc_summary=nvc_summary,
                        conversation_complete=True
                    )
                
                # Get AI response
                prompt = get_nvc_prompt(request.message, request.context, conversation_history)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a skilled NVC facilitator."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content.strip()
                
                # Use AI to detect current step with conversation context
                current_step = detect_nvc_step_with_ai(request.message, conversation_history)
                next_step = get_next_nvc_step(current_step)
                
                # Get vocabulary and suggestions
                vocabulary = get_nvc_vocabulary_for_step(next_step)
                suggestions = get_generic_suggestions(next_step)
                
                return ConversationResponse(
                    response=ai_response,
                    current_step=next_step,
                    guidance="AI-powered NVC guidance",
                    example="Response generated by GPT-4o-mini",
                    suggested_responses=suggestions,
                    vocabulary_options=vocabulary
                )
                
            except Exception:
                # Fall back to rule-based logic
                pass
        
        # Rule-based fallback
        conversation_history = request.conversation_history or []
        conversation_history.append(request.message)
        
        # Use AI to check if conversation should complete
        if ai_should_complete_conversation(conversation_history):
            context = analyze_user_context(request.message)
            nvc_summary = generate_nvc_summary(conversation_history, context)
            
            return ConversationResponse(
                response="Great work! You've completed all four steps of NVC. Here's your summary:",
                current_step="complete",
                guidance="Conversation complete - here's your NVC summary",
                example="Use this structure when talking to your executive director",
                suggested_responses=[],
                vocabulary_options=[],
                nvc_summary=nvc_summary,
                conversation_complete=True
            )
        
        # Use AI step detection for rule-based fallback too
        current_step = detect_nvc_step_with_ai(request.message, conversation_history)
        next_step = get_next_nvc_step(current_step)
        
        # Simple step responses
        step_responses = {
            "observation": {
                "ai_response": "I hear you describing what you observed. Can you tell me more about what you're feeling about this situation?",
                "guidance": "Great start with observation! Try to stick to facts without evaluation.",
                "example": "Instead of 'He was being rude' try 'He interrupted me twice during our conversation'"
            },
            "feeling": {
                "ai_response": "Thank you for sharing your feelings. What do you think you need in this situation?",
                "guidance": "You're expressing feelings - this is important for connection.",
                "example": "Try using feeling words like: frustrated, excited, worried, grateful, confused"
            },
            "need": {
                "ai_response": "I understand your needs better now. What specific request could you make to meet this need?",
                "guidance": "You're identifying your needs - this gets to the heart of NVC.",
                "example": "Universal needs might include: understanding, respect, connection, autonomy, safety"
            },
            "request": {
                "ai_response": "That sounds like a clear request. How do you think this request might help meet your needs?",
                "guidance": "You're making a request - make sure it's specific and doable.",
                "example": "Make requests specific and positive: 'Would you be willing to listen for 5 minutes?' rather than 'Don't interrupt me'"
            }
        }
        
        response_data = step_responses.get(next_step, {
            "ai_response": "Let's work through this together step by step.",
            "guidance": "NVC helps us connect with needs and find solutions.",
            "example": "Start with what you observed without judgment."
        })
        
        vocabulary = get_nvc_vocabulary_for_step(next_step)
        suggestions = get_generic_suggestions(next_step)
        
        return ConversationResponse(
            response=response_data["ai_response"],
            current_step=next_step,
            guidance=response_data["guidance"],
            example=response_data["example"],
            suggested_responses=suggestions,
            vocabulary_options=vocabulary
        )
        
    except Exception as e:
        logger.error(f"NVC conversation error: {e}")
        # Basic fallback
        return ConversationResponse(
            response="I understand you'd like to work through this situation using NVC. Let's start with what you observed.",
            current_step="observation",
            guidance="Start with facts, not interpretations",
            example="I noticed... I heard... I saw...",
            suggested_responses=["I noticed that...", "What I observed was...", "I heard..."],
            vocabulary_options=["noticed", "observed", "heard", "saw"]
        )

@router.get("/feelings")
async def get_feelings_list():
    """Get list of NVC feelings vocabulary."""
    feelings = {
        "when_needs_met": [
            "grateful", "happy", "excited", "peaceful", "confident", "hopeful",
            "joyful", "content", "fulfilled", "energized", "inspired", "relieved"
        ],
        "when_needs_not_met": [
            "angry", "frustrated", "sad", "worried", "confused", "disappointed",
            "hurt", "scared", "lonely", "overwhelmed", "irritated", "anxious"
        ]
    }
    return feelings

@router.get("/needs")
async def get_needs_list():
    """Get list of universal human needs."""
    needs = {
        "connection": ["love", "friendship", "intimacy", "community", "belonging"],
        "physical": ["safety", "shelter", "food", "rest", "health", "exercise"],
        "autonomy": ["choice", "freedom", "independence", "self-expression", "creativity"],
        "meaning": ["purpose", "growth", "learning", "contribution", "understanding"],
        "celebration": ["joy", "beauty", "fun", "play", "humor", "hope"]
    }
    return needs

@router.get("/examples")
async def get_nvc_examples():
    """Get NVC practice examples."""
    examples = {
        "full_example": {
            "observation": "When I see you checking your phone during our conversation",
            "feeling": "I feel disconnected and frustrated",
            "need": "because I need presence and connection when we talk",
            "request": "Would you be willing to put your phone away while we're talking?"
        },
        "tips": [
            "Start with 'When I see/hear...' for observations",
            "Use 'I feel...' followed by actual emotions, not thoughts",
            "Connect feelings to universal human needs",
            "Make requests specific, positive, and doable"
        ]
    }
    return examples