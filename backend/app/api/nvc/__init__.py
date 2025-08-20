"""
NVC resources and guidance API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from openai import OpenAI

router = APIRouter()

class ConversationRequest(BaseModel):
    message: str
    context: Optional[str] = None
    nvc_step: Optional[str] = None  # observation, feeling, need, request
    conversation_history: Optional[List[str]] = []

class ConversationResponse(BaseModel):
    ai_response: str
    suggested_nvc_step: str
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
    """Use AI to analyze the user's message and extract contextual information for better suggestions."""
    
    # Temporarily disable AI analysis on Railway to fix 500 errors
    if os.getenv("RAILWAY_ENVIRONMENT"):
        logger.info("Railway environment detected, using fallback context analysis")
        return fallback_context_analysis(message)
    
    try:
        from openai import OpenAI
        import os
        import json
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("No OpenAI API key found, using fallback context analysis")
            return fallback_context_analysis(message)
            
        client = OpenAI(api_key=api_key)
        
        prompt = f"""Analyze this message and extract key context information. Return ONLY a JSON object with these fields:
- "person": who they're referring to (coworker, boss, partner, friend, family member, teammate, etc.)
- "relationship": the relationship type (professional, personal, family, etc.) 
- "setting": where this happened (work, meeting, home, phone call, etc.)
- "action": what the other person did (interrupted, dismissed, ignored, took credit, etc.)
- "emotion": the user's emotional state (frustrated, hurt, angry, disappointed, etc.)

Message: "{message}"

Return only valid JSON, no other text."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a context extraction tool. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )
        
        # Clean and parse the response
        raw_content = response.choices[0].message.content.strip()
        logger.info(f"Raw AI response: {raw_content}")
        
        # Remove any markdown code blocks if present
        if raw_content.startswith("```"):
            raw_content = raw_content.split("```")[1]
            if raw_content.startswith("json"):
                raw_content = raw_content[4:]
        
        context = json.loads(raw_content)
        logger.info(f"AI extracted context: {context}")
        
        # Ensure all required fields exist with defaults
        context.setdefault("person", "colleague")
        context.setdefault("relationship", "professional")
        context.setdefault("setting", "situation")
        context.setdefault("action", "behaving this way")
        context.setdefault("emotion", "frustrated")
        
        return context
        
    except Exception as e:
        logger.warning(f"AI context analysis failed: {e}, using fallback")
        return fallback_context_analysis(message)

def fallback_context_analysis(message: str) -> dict:
    """Fallback context analysis using pattern matching when AI fails."""
    message_lower = message.lower()
    
    context = {
        "person": "colleague",
        "relationship": "professional", 
        "setting": "situation",
        "action": "behaving this way",
        "emotion": "frustrated"
    }
    
    # Identify person
    if "manager" in message_lower or "boss" in message_lower:
        context["person"] = "manager"
    elif "colleague" in message_lower or "coworker" in message_lower:
        context["person"] = "colleague"
    elif "partner" in message_lower or "spouse" in message_lower:
        context["person"] = "partner"
        context["relationship"] = "personal"
    elif "friend" in message_lower:
        context["person"] = "friend"
        context["relationship"] = "personal"
    
    # Identify setting
    if "meeting" in message_lower:
        context["setting"] = "meeting"
    elif "work" in message_lower or "office" in message_lower:
        context["setting"] = "work"
    elif "home" in message_lower:
        context["setting"] = "home"
    
    return context

def generate_contextual_suggestions(step: str, user_message: str, context: dict = None) -> List[str]:
    """Generate highly contextual NVC response suggestions based on the user's specific situation."""
    
    if not context:
        context = analyze_user_context(user_message)
    
    # Use safe defaults and handle None values
    person = context.get("person") or "colleague"
    action = context.get("action") or "behaved"
    setting = context.get("setting") or "situation"
    
    # Remove "my" prefix when person is None or unclear
    person_phrase = person if person in ["colleague", "coworker", "teammate", "friend", "partner"] else "they"
    possessive_person = f"my {person}" if person not in ["they", "someone"] else person
    
    suggestions = {
        "observation": [
            f"I noticed that {possessive_person} interrupted me three times during our {setting}",
            f"I observed that {possessive_person} didn't acknowledge my contributions", 
            f"What happened was that {possessive_person} spoke over me while I was presenting"
        ],
        "feeling": [
            f"I feel frustrated when {person_phrase} interrupts me",
            f"I'm feeling unheard and undervalued in our {setting}",
            f"I feel disappointed when my ideas aren't acknowledged"
        ],
        "need": [
            f"I need respect and recognition for my contributions",
            f"I value being heard and having my voice matter",
            f"I need collaboration and mutual respect in our {setting}"
        ],
        "request": [
            f"Would you be willing to let me finish my thoughts before responding?",
            f"Could we establish a way for me to contribute without interruption?",
            f"I'd appreciate if you could acknowledge my input during our {setting}s"
        ]
    }
    
    # Fallback to generic suggestions if context is unclear
    generic_suggestions = {
        "observation": [
            "I noticed that...",
            "What I observed was...",
            "The facts are that..."
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
    
    return suggestions.get(step, generic_suggestions.get(step, []))

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
    step_sequence = ["observation", "feeling", "need", "request", "complete"]
    
    if current_step == "starting":
        return "observation"
    elif current_step in step_sequence:
        current_index = step_sequence.index(current_step)
        if current_index < len(step_sequence) - 1:
            return step_sequence[current_index + 1]
    
    return "complete"

def should_complete_conversation(conversation_history: List[str]) -> bool:
    """Determine if the conversation has covered all NVC steps and should complete."""
    if len(conversation_history) < 4:  # Need at least some back-and-forth
        return False
    
    # Check if we have evidence of all four steps
    all_messages = " ".join(conversation_history)
    
    has_observation = any(word in all_messages.lower() for word in ["noticed", "saw", "heard", "observed"])
    has_feeling = any(word in all_messages.lower() for word in ["feel", "feeling", "frustrated", "sad", "angry"])
    has_need = any(word in all_messages.lower() for word in ["need", "value", "respect", "understanding"])
    has_request = any(word in all_messages.lower() for word in ["would you", "could", "please", "request"])
    
    return has_observation and has_feeling and has_need and has_request

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
    NVC AI conversation endpoint with OpenAI integration.
    Falls back to rule-based logic if OpenAI is not configured.
    """
    try:
        client = get_openai_client()
        
        if client:
            # Use OpenAI for sophisticated NVC guidance
            try:
                conversation_history = request.conversation_history or []
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
                
                # Detect current step and determine next step
                current_step = detect_current_nvc_step(request.message)
                next_step = get_next_nvc_step(current_step)
                
                # Check if conversation should complete
                conversation_history = request.conversation_history or []
                conversation_history.append(request.message)
                
                if should_complete_conversation(conversation_history) or next_step == "complete":
                    # Generate final NVC summary
                    context = analyze_user_context(request.message)
                    nvc_summary = generate_nvc_summary(conversation_history, context)
                    
                    return ConversationResponse(
                        ai_response=ai_response,
                        suggested_nvc_step="complete",
                        guidance="Conversation complete - here's your NVC summary",
                        example="Response generated by GPT-4o-mini",
                        suggested_responses=[],
                        vocabulary_options=[],
                        nvc_summary=nvc_summary,
                        conversation_complete=True
                    )
                
                # Get suggestions for NEXT step (not current)
                context = analyze_user_context(request.message)
                vocabulary = get_nvc_vocabulary_for_step(next_step)
                suggestions = generate_contextual_suggestions(next_step, request.message, context)
                
                return ConversationResponse(
                    ai_response=ai_response,
                    suggested_nvc_step=next_step,
                    guidance="OpenAI-powered NVC guidance",
                    example="Response generated by GPT-4o-mini",
                    suggested_responses=suggestions,
                    vocabulary_options=vocabulary
                )
                
            except Exception as openai_error:
                # Fall back to rule-based if OpenAI fails
                pass
        
        # Rule-based fallback with improved step detection
        current_step = detect_current_nvc_step(request.message)
        next_step = get_next_nvc_step(current_step)
        
        # Check if conversation should complete
        conversation_history = request.conversation_history or []
        conversation_history.append(request.message)
        
        if should_complete_conversation(conversation_history) or next_step == "complete":
            # Generate final NVC summary
            context = analyze_user_context(request.message)
            nvc_summary = generate_nvc_summary(conversation_history, context)
            
            return ConversationResponse(
                ai_response="Based on our conversation, I've created a complete NVC framework for your situation. This gives you a clear structure to address the issue constructively.",
                suggested_nvc_step="complete",
                guidance="Conversation complete - here's your NVC summary (Rule-based fallback)",
                example="Use this structure when talking to the other person",
                suggested_responses=[],
                vocabulary_options=[],
                nvc_summary=nvc_summary,
                conversation_complete=True
            )
        
        # Generate responses based on next step
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
            "ai_response": "I'd like to help you work through this using NVC. Can you start by telling me what you observed - just the facts of what happened?",
            "guidance": "Let's start with what you observed. What exactly happened?",
            "example": "NVC has 4 steps: Observation, Feelings, Needs, and Requests"
        })
        
        # Get suggestions for next step
        context = analyze_user_context(request.message)
        vocabulary = get_nvc_vocabulary_for_step(next_step)
        suggestions = generate_contextual_suggestions(next_step, request.message, context)
        
        return ConversationResponse(
            ai_response=response_data["ai_response"],
            suggested_nvc_step=next_step,
            guidance=response_data["guidance"] + " (Rule-based fallback)",
            example=response_data["example"],
            suggested_responses=suggestions,
            vocabulary_options=vocabulary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing conversation: {str(e)}")

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