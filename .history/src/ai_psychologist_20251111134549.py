"""
AI Psychologist with Long-Term Memory Implementation
"""

import os
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

from config import Config

class OpenRouterClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.client = OpenAI(
            base_url=Config.OPENROUTER_BASE_URL,
            api_key=self.api_key
        )
    
    def chat_completion(self, messages: List[Dict[str, str]], model: str = None) -> Dict[str, Any]:
        """
        Implementation of OpenRouter chat completion API
        """
        if model is None:
            model = Config.DEFAULT_MODEL
            
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response.choices[0].message.content
                    }
                }]
            }
        except Exception as e:
            # Fallback to mock response if API fails
            print(f"Warning: API call failed, using mock response: {e}")
            return self._mock_response(messages)
    
    def _mock_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Mock implementation for fallback when API is not available
        """
        # Simple response generation based on the last user message
        user_message = messages[-1]["content"] if messages else ""
        
        # Simple empathetic responses based on keywords
        responses = {
            "sad": "I can sense that you're feeling down. It's okay to feel this way, and I'm here to support you.",
            "depress": "I hear that you're going through a difficult time. Depression can be challenging, but you're not alone.",
            "anxious": "Anxiety can be overwhelming. Let's take a deep breath together and explore what might be causing these feelings.",
            "happy": "It's wonderful to hear that you're feeling positive! What's been contributing to your happiness lately?",
            "stress": "Stress can take a toll on us. Let's identify what's causing your stress and find ways to manage it.",
            "angry": "Anger is a natural emotion. Let's explore what's triggering these feelings and find healthy ways to express them.",
            "lonely": "Feeling lonely can be difficult. You're not alone in this, and I'm here to provide companionship and support.",
        }
        
        # Default empathetic response
        response_text = "I hear you and I'm here to support you. Could you tell me more about what you're experiencing?"
        
        # Try to match keywords in the user message
        user_message_lower = user_message.lower()
        for keyword, response in responses.items():
            if keyword in user_message_lower:
                response_text = response
                break
        
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response_text
                }
            }]
        }

class MemorySystem:
    """Multi-layered memory system for the AI Psychologist"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.storage_path = Config.DATA_STORAGE_PATH
        self.user_dir = os.path.join(self.storage_path, user_id)
        
        # Create user directory if it doesn't exist
        os.makedirs(self.user_dir, exist_ok=True)
        
        # Initialize vector database for semantic memory
        self._init_vector_db()
        
        # Initialize memory layers
        self.working_memory = []  # Short-term conversation context
        self.episodic_memory = []  # Time-stamped events and experiences
        self.semantic_memory = {}  # Facts, knowledge, and user profile
        
        # Load existing memories
        self._load_memories()
    
    def _init_vector_db(self):
        """Initialize the vector database for semantic memory"""
        try:
            chroma_client = chromadb.PersistentClient(path=Config.VECTOR_DB_PATH)
            self.collection = chroma_client.get_or_create_collection(
                name=f"user_{self.user_id}_memories",
                embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
        except Exception as e:
            print(f"Warning: Could not initialize vector database: {e}")
            self.collection = None
    
    def _load_memories(self):
        """Load existing memories from storage"""
        # Load semantic memory (user profile and facts)
        semantic_file = os.path.join(self.user_dir, "semantic_memory.json")
        if os.path.exists(semantic_file):
            try:
                with open(semantic_file, 'r', encoding='utf-8') as f:
                    self.semantic_memory = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load semantic memory: {e}")
        
        # Load episodic memory (past conversations)
        episodic_file = os.path.join(self.user_dir, "episodic_memory.json")
        if os.path.exists(episodic_file):
            try:
                with open(episodic_file, 'r', encoding='utf-8') as f:
                    self.episodic_memory = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load episodic memory: {e}")
    
    def save_memories(self):
        """Save all memories to persistent storage"""
        # Save semantic memory
        semantic_file = os.path.join(self.user_dir, "semantic_memory.json")
        try:
            with open(semantic_file, 'w', encoding='utf-8') as f:
                json.dump(self.semantic_memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving semantic memory: {e}")
        
        # Save episodic memory
        episodic_file = os.path.join(self.user_dir, "episodic_memory.json")
        try:
            with open(episodic_file, 'w', encoding='utf-8') as f:
                json.dump(self.episodic_memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving episodic memory: {e}")
    
    def add_working_memory(self, message: Dict[str, str]):
        """Add a message to working memory"""
        self.working_memory.append({
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "message": message
        })
        
        # Keep only the last N messages in working memory
        if len(self.working_memory) > Config.WORKING_MEMORY_SIZE:
            self.working_memory = self.working_memory[-Config.WORKING_MEMORY_SIZE:]
    
    def add_episodic_memory(self, event: Dict[str, Any]):
        """Add an event to episodic memory"""
        event_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            **event
        }
        self.episodic_memory.append(event_entry)
        
        # Add to vector database if available
        if self.collection and "summary" in event:
            try:
                self.collection.add(
                    documents=[event["summary"]],
                    metadatas=[event],
                    ids=[event_entry["id"]]
                )
            except Exception as e:
                print(f"Warning: Could not add to vector database: {e}")
        
        # Save to persistent storage
        self.save_memories()
    
    def update_semantic_memory(self, key: str, value: Any):
        """Update semantic memory with a key-value pair"""
        self.semantic_memory[key] = value
        self.save_memories()
    
    def get_working_memory_context(self) -> List[Dict[str, str]]:
        """Get the current working memory as context"""
        return [item["message"] for item in self.working_memory]
    
    def get_relevant_episodic_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get relevant episodic memories based on a query"""
        if self.collection:
            try:
                # Search in vector database
                results = self.collection.query(
                    query_texts=[query],
                    n_results=min(limit, len(self.episodic_memory)) if self.episodic_memory else 1
                )
                
                if results["metadatas"] and results["metadatas"][0]:
                    return results["metadatas"][0]
            except Exception as e:
                print(f"Warning: Vector database query failed: {e}")
        
        # Fallback to returning most recent memories
        return self.episodic_memory[-limit:] if self.episodic_memory else []
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get the user profile from semantic memory"""
        return self.semantic_memory.get("user_profile", {})
    
    def reset_memory(self):
        """Reset all memory for the user"""
        self.working_memory = []
        self.episodic_memory = []
        self.semantic_memory = {}
        
        # Clear vector database collection
        if self.collection:
            try:
                self.collection.delete(ids=[mem["id"] for mem in self.episodic_memory])
            except Exception as e:
                print(f"Warning: Could not clear vector database: {e}")
        
        # Remove memory files
        for filename in ["semantic_memory.json", "episodic_memory.json"]:
            file_path = os.path.join(self.user_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Warning: Could not remove {filename}: {e}")

class AIPsychologist:
    """Main AI Psychologist class with long-term memory capabilities"""
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.llm_client = OpenRouterClient()
        self.memory_system = MemorySystem(user_id)
        
        # Initialize with a default personality
        self.personality = "empathetic"
        
        # Initialize user profile if it doesn't exist
        if not self.memory_system.get_user_profile():
            self.memory_system.update_semantic_memory("user_profile", {
                "preferences": {},
                "psychological_history": [],
                "personality_insights": {}
            })
    
    def _extract_emotional_insights(self, user_message: str) -> Dict[str, Any]:
        """Extract emotional insights from user message (simplified)"""
        # In a real implementation, this would use sentiment analysis and NLP
        insights = {
            "emotions": [],
            "topics": [],
            "intensity": 0
        }
        
        # Simple keyword-based emotion detection
        emotions = {
            "sadness": ["sad", "depressed", "unhappy", "down", "blue", "depression"],
            "anxiety": ["anxious", "worried", "nervous", "stressed", "concerned", "panic"],
            "anger": ["angry", "mad", "frustrated", "irritated", "annoyed", "rage"],
            "happiness": ["happy", "joy", "pleased", "delighted", "excited", "glad"],
            "loneliness": ["lonely", "alone", "isolated", "by myself", "solitude"]
        }
        
        user_message_lower = user_message.lower()
        for emotion, keywords in emotions.items():
            for keyword in keywords:
                if keyword in user_message_lower:
                    insights["emotions"].append(emotion)
                    insights["intensity"] = max(insights["intensity"], len(keyword))
        
        return insights
    
    def _build_context(self, user_message: str) -> List[Dict[str, str]]:
        """Build context for the LLM using multi-layered memory"""
        # Start with working memory (recent conversation)
        context = self.memory_system.get_working_memory_context()
        
        # Add relevant episodic memories
        relevant_memories = self.memory_system.get_relevant_episodic_memories(user_message)
        if relevant_memories:
            memory_summary = "Relevant past conversations:\n"
            for mem in relevant_memories[-3:]:  # Last 3 memories
                memory_summary += f"- {mem.get('summary', 'Conversation')}\n"
            
            context.insert(0, {
                "role": "system",
                "content": f"Previous context: {memory_summary}"
            })
        
        # Add user profile information
        user_profile = self.memory_system.get_user_profile()
        if user_profile:
            profile_info = f"User profile: {json.dumps(user_profile, ensure_ascii=False)}"
            context.insert(0, {
                "role": "system",
                "content": profile_info
            })
        
        # Add the current user message
        context.append({
            "role": "user",
            "content": user_message
        })
        
        return context
    
    def _update_memory(self, user_message: str, ai_response: str):
        """Update memory systems with the current interaction"""
        # Add to working memory
        self.memory_system.add_working_memory({
            "role": "user",
            "content": user_message
        })
        
        self.memory_system.add_working_memory({
            "role": "assistant",
            "content": ai_response
        })
        
        # Extract and store emotional insights
        emotional_insights = self._extract_emotional_insights(user_message)
        
        # Add to episodic memory
        self.memory_system.add_episodic_memory({
            "interaction": {
                "user_message": user_message,
                "ai_response": ai_response,
                "emotional_insights": emotional_insights
            },
            "summary": f"User expressed {', '.join(emotional_insights['emotions']) if emotional_insights['emotions'] else 'feelings'}"
        })
        
        # Update semantic memory with user preferences and insights
        user_profile = self.memory_system.get_user_profile()
        if emotional_insights["emotions"]:
            # Update personality insights
            personality_insights = user_profile.get("personality_insights", {})
            for emotion in emotional_insights["emotions"]:
                personality_insights[emotion] = personality_insights.get(emotion, 0) + 1
            
            user_profile["personality_insights"] = personality_insights
            self.memory_system.update_semantic_memory("user_profile", user_profile)
    
    def chat(self, user_message: str) -> str:
        """Process a user message and generate a response"""
        # Build context using multi-layered memory
        context = self._build_context(user_message)
        
        # Get response from LLM
        response = self.llm_client.chat_completion(context)
        ai_response = response["choices"][0]["message"]["content"]
        
        # Update memory with this interaction
        self._update_memory(user_message, ai_response)
        
        return ai_response
    
    def reset_memory(self):
        """Reset all memory for the user"""
        self.memory_system.reset_memory()


# Example usage
if __name__ == "__main__":
    # Create an instance of the AI Psychologist
    psychologist = AIPsychologist("test_user")
    
    # Example conversation
    print("AI Psychologist Demo")
    print("=" * 30)
    
    test_messages = [
        "I've been feeling really sad lately.",
        "It's because I lost my job last month.",
        "I'm worried about how I'll pay my bills."
    ]
    
    for message in test_messages:
        response = psychologist.chat(message)
        print(f"You: {message}")
        print(f"AI Psychologist: {response}\n")