"""
AI Psychologist with Long-Term Memory Implementation
"""

import os
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

# Conditional imports - only import if available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    chromadb = None
    embedding_functions = None

from config import Config
from procedural_memory import procedural_memory

class OpenRouterClient:
    def __init__(self, api_key: Optional[str] = None):
        if OPENAI_AVAILABLE:
            self.api_key = api_key or Config.OPENROUTER_API_KEY
            self.client = OpenAI(
                base_url=Config.OPENROUTER_BASE_URL,
                api_key=self.api_key
            )
        else:
            self.api_key = api_key or Config.OPENROUTER_API_KEY
            self.client = None
    
    def chat_completion(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> Dict[str, Any]:
        """
        Implementation of OpenRouter chat completion API
        """
        if model is None:
            model = Config.DEFAULT_MODEL
            
        # Use real API if available, otherwise fallback to mock
        if OPENAI_AVAILABLE and self.client:
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
        else:
            # Use mock response if OpenAI not available
            return self._mock_response(messages)
    
    def _mock_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Mock implementation for fallback when API is not available
        """
        # Simple response generation based on the last user message
        user_message = messages[-1]["content"] if messages else ""
        
        # Simple empathetic responses based on keywords
        responses = {
            "sad": "我感觉到你有些难过。有这种感觉很正常，我会陪伴你一起面对。",
            "depress": "我听到你正在经历困难时期。抑郁确实很有挑战性，但你并不孤单。",
            "anxious": "焦虑会让人感到不堪重负。让我们一起深呼吸，探索一下是什么引起了这些感受。",
            "happy": "很高兴听到你感到积极！是什么让你感到快乐呢？",
            "stress": "压力确实会对我们产生影响。让我们找出压力的来源，并找到应对的方法。",
            "angry": "愤怒是一种自然的情绪。让我们探索一下是什么触发了这些感受，并找到健康的方式来表达它们。",
            "lonely": "感到孤独确实很难受。你并不孤单，我会陪伴你并提供支持。",
        }
        
        # Default empathetic response
        response_text = "我听到了你的话，我会陪伴你一起面对。你能告诉我更多关于你的感受吗？"
        
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
        if CHROMA_AVAILABLE:
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
        else:
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
            "sadness": ["sad", "depressed", "unhappy", "down", "blue", "depression", "难过", "沮丧"],
            "anxiety": ["anxious", "worried", "nervous", "stressed", "concerned", "panic", "焦虑", "担心"],
            "anger": ["angry", "mad", "frustrated", "irritated", "annoyed", "rage", "愤怒", "生气"],
            "happiness": ["happy", "joy", "pleased", "delighted", "excited", "glad", "高兴", "快乐"],
            "loneliness": ["lonely", "alone", "isolated", "by myself", "solitude", "孤独"]
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
        
        # Add relevant therapeutic techniques based on user message
        relevant_techniques = procedural_memory.get_relevant_techniques(user_message)
        if relevant_techniques:
            technique_info = "可用的治疗技术:\n"
            for name, technique in list(relevant_techniques.items())[:3]:  # Limit to 3 techniques
                technique_info += procedural_memory.format_technique_for_prompt(name, technique) + "\n"
            
            context.insert(0, {
                "role": "system",
                "content": f"治疗技术参考:\n{technique_info}"
            })
        
        # Add relevant episodic memories
        relevant_memories = self.memory_system.get_relevant_episodic_memories(user_message)
        if relevant_memories:
            memory_summary = "相关的过往对话:\n"
            for mem in relevant_memories[-3:]:  # Last 3 memories
                memory_summary += f"- {mem.get('summary', '对话')}\n"
            
            context.insert(0, {
                "role": "system",
                "content": f"历史背景: {memory_summary}"
            })
        
        # Add user profile information
        user_profile = self.memory_system.get_user_profile()
        if user_profile:
            profile_info = f"用户档案: {json.dumps(user_profile, ensure_ascii=False)}"
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
            "summary": f"用户表达了 {', '.join(emotional_insights['emotions']) if emotional_insights['emotions'] else '感受'}"
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
    print("AI心理学家演示")
    print("=" * 30)
    
    test_messages = [
        "我最近感到很焦虑。",
        "主要是因为即将到来的工作面试。",
        "我担心表现不好会让家人失望。"
    ]
    
    for message in test_messages:
        response = psychologist.chat(message)
        print(f"你: {message}")
        print(f"AI心理学家: {response}\n")