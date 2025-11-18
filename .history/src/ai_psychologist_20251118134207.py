#!/usr/bin/env python3
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

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

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

class OllamaClient:
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        self.model = model or Config.OLLAMA_MODEL
        self.available = REQUESTS_AVAILABLE
    
    def chat_completion(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> Dict[str, Any]:
        """
        Implementation of Ollama chat completion API
        """
        if not self.available:
            return self._mock_response(messages)
        
        model_name = model or self.model
        
        # Format messages for Ollama
        ollama_messages = []
        for msg in messages:
            ollama_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model_name,
                    "messages": ollama_messages,
                    "stream": False
                },
                timeout=120  # 2分钟超时
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "choices": [{
                        "message": {
                            "role": "assistant",
                            "content": data["message"]["content"]
                        }
                    }]
                }
            else:
                print(f"Warning: Ollama API call failed with status {response.status_code}")
                return self._mock_response(messages)
        except Exception as e:
            print(f"Warning: Ollama API call failed, using mock response: {e}")
            return self._mock_response(messages)
    
    def _mock_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Mock implementation for fallback when Ollama is not available
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

class LLMClient:
    """统一的LLM客户端，支持多种模型提供商"""
    
    def __init__(self):
        self.provider = Config.MODEL_PROVIDER.lower()
        
        if self.provider == "openrouter":
            self.client = OpenRouterClient()
        elif self.provider == "ollama":
            self.client = OllamaClient()
        else:
            # 默认使用OpenRouter
            self.client = OpenRouterClient()
            self.provider = "openrouter"
    
    def chat_completion(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> Dict[str, Any]:
        """
        统一的聊天完成接口
        """
        return self.client.chat_completion(messages, model)

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
                # 尝试使用国内镜像源
                try:
                    self.collection = chroma_client.get_or_create_collection(
                        name=f"user_{self.user_id}_memories",
                        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                            model_name="all-MiniLM-L6-v2"
                        )
                    )
                except Exception as e:
                    print(f"Warning: Could not initialize vector database with default model: {e}")
                    # 降级到基本的文本匹配，不使用向量数据库
                    self.collection = None
            except Exception as e:
                print(f"Warning: Could not initialize vector database: {e}")
                print("Semantic memory will be stored in JSON files only.")
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
                # 将复杂对象转换为字符串以避免向量数据库错误
                metadata = {
                    "summary": event["summary"],
                    "timestamp": event_entry["timestamp"],
                    "datetime": event_entry["datetime"]
                }
                
                # 如果有交互信息，将其转换为字符串
                if "interaction" in event:
                    interaction_str = json.dumps(event["interaction"], ensure_ascii=False)
                    metadata["interaction"] = interaction_str
                
                self.collection.add(
                    documents=[event["summary"]],
                    metadatas=[metadata],  # 使用简化后的metadata
                    ids=[event_entry["id"]]
                )
            except Exception as e:
                print(f"Warning: Could not add to vector database: {e}")
        
        # Save to persistent storage
        self.save_memories()
    
    def add_time_based_episodic_memory(self, time_ref: str, event_details: Dict[str, Any]):
        """添加基于时间参考的情景记忆"""
        # 解析时间参考
        timestamp = self._parse_time_reference(time_ref)
        if not timestamp:
            print(f"无法解析时间参考: {time_ref}")
            return
        
        # 创建时间点记录，使用统一的数据结构
        event_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat() if timestamp else datetime.now().isoformat(),
            "time_reference": time_ref,  # 添加时间参考字段
            "interaction": {
                "user_message": event_details.get("user_message", ""),
                "ai_response": event_details.get("ai_response", ""),
                "emotional_insights": event_details.get("emotional_insights", {})
            },
            "activity": event_details.get("activity", "其他活动"),  # 添加活动字段
            "summary": self._summarize_time_events([event_details])
        }
        
        # 检查是否已存在该时间点的记忆
        existing_index = None
        for i, memory in enumerate(self.episodic_memory):
            if abs(memory["timestamp"] - timestamp) < 24 * 60 * 60:  # 24小时容差
                existing_index = i
                break
        
        if existing_index is not None:
            # 合并事件详情，使用统一的数据结构
            existing = self.episodic_memory[existing_index]
            
            # 确保existing有统一的结构
            if "interaction" not in existing:
                existing["interaction"] = {
                    "user_message": "",
                    "ai_response": "",
                    "emotional_insights": {}
                }
            
            # 添加时间参考字段（如果不存在）
            if "time_reference" not in existing:
                existing["time_reference"] = time_ref
            
            # 添加活动字段（如果不存在）
            if "activity" not in existing:
                existing["activity"] = "其他活动"
            
            # 添加新的交互记录到现有记录中
            # 注意：这里我们保持单个interaction，而不是details数组
            # 如果需要记录多个交互，可以考虑其他方式
            existing["interaction"] = {
                "user_message": event_details.get("user_message", ""),
                "ai_response": event_details.get("ai_response", ""),
                "emotional_insights": event_details.get("emotional_insights", {})
            }
            
            # 更新活动信息
            existing["activity"] = event_details.get("activity", existing.get("activity", "其他活动"))
            
            # 重新生成摘要
            existing["summary"] = self._summarize_time_events([event_details])
        else:
            # 添加新的时间点记录
            self.episodic_memory.append(event_entry)
        
        # 保存到持久化存储
        self.save_memories()
        
        # 添加到向量数据库（如果可用）
        if self.collection:
            try:
                self.collection.add(
                    documents=[event_entry["summary"]],
                    metadatas=[{
                        "summary": event_entry["summary"],
                        "timestamp": event_entry["timestamp"],
                        "time_reference": event_entry["time_reference"],
                        "datetime": event_entry["datetime"]
                    }],
                    ids=[event_entry["id"]]
                )
            except Exception as e:
                print(f"Warning: Could not add to vector database: {e}")

    def _summarize_time_events(self, events: List[Dict[str, Any]]) -> str:
        """自动总结时间点事件"""
        # 简单实现：连接所有事件的关键信息
        summary_parts = []
        for event in events:
            if "emotional_insights" in event and event["emotional_insights"].get("emotions"):
                summary_parts.append(f"表达了{', '.join(event['emotional_insights']['emotions'])}")
            if "activity" in event:
                summary_parts.append(f"进行了{event['activity']}")
        
        return "；".join(summary_parts) if summary_parts else "发生了某些事件"

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
                    # 将字符串化的交互信息转换回字典
                    metadatas = results["metadatas"][0]
                    for metadata in metadatas:
                        if "interaction" in metadata and isinstance(metadata["interaction"], str):
                            try:
                                metadata["interaction"] = json.loads(metadata["interaction"])
                            except:
                                pass  # 如果转换失败，保持原样
                    return metadatas
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
    
    def _extract_time_reference(self, user_message: str) -> Optional[str]:
        """从用户消息中提取时间参考"""
        import re
        
        # 时间表达式模式
        patterns = [
            r'昨天', r'今天', r'明天', r'前天', r'大前天',
            r'上周', r'这周', r'下周',
            r'上个月', r'这个月', r'下个月',
            r'去年', r'今年', r'明年',
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # YYYY年MM月DD日
            r'(\d{1,2})月(\d{1,2})日',           # MM月DD日
            r'(\d{4})-(\d{1,2})-(\d{1,2})',      # YYYY-MM-DD
            r'(\d{1,2})/(\d{1,2})/(\d{4})',      # MM/DD/YYYY
            r'暑假', r'寒假', r'春节'  # 特殊时间点
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_message)
            if match:
                return match.group(0)
        
        return None

    def _parse_time_reference(self, time_ref: str) -> Optional[float]:
        """将时间参考解析为时间戳"""
        from datetime import datetime, timedelta
        import re
        
        now = datetime.now()
        
        # 相对时间
        if time_ref == '昨天':
            return (now - timedelta(days=1)).timestamp()
        elif time_ref == '今天':
            return now.timestamp()
        elif time_ref == '前天':
            return (now - timedelta(days=2)).timestamp()
        elif time_ref == '去年':
            return (now - timedelta(days=365)).timestamp()
        elif time_ref == '今年':
            return now.timestamp()  # 今年应该返回年初的时间戳
        elif time_ref == '暑假':
            # 假设暑假是7-8月
            return now.replace(month=7, day=1).timestamp()
        elif time_ref == '寒假':
            # 假设寒假是1-2月
            return now.replace(month=1, day=1).timestamp()
        
        # 绝对时间
        date_patterns = [
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
        ]
        
        for pattern in date_patterns:
            match = re.match(pattern, time_ref)
            if match:
                try:
                    if pattern == date_patterns[0]:  # YYYY年MM月DD日
                        year, month, day = map(int, match.groups())
                    elif pattern == date_patterns[1]:  # YYYY-MM-DD
                        year, month, day = map(int, match.groups())
                    else:  # MM/DD/YYYY
                        month, day, year = map(int, match.groups())
                    
                    date = datetime(year, month, day)
                    return date.timestamp()
                except:
                    continue
        
        return None

    def get_episodic_memory_by_time(self, time_ref: str) -> Optional[Dict[str, Any]]:
        """根据时间参考获取情景记忆"""
        timestamp = self._parse_time_reference(time_ref)
        if not timestamp:
            return None
        
        # 查找最接近的时间点（允许一定的时间误差）
        tolerance = 24 * 60 * 60  # 24小时容差
        best_match = None
        best_diff = float('inf')
        
        for memory in self.episodic_memory:
            # 检查记忆是否有时间参考字段并且匹配
            if "time_reference" in memory and memory["time_reference"] == time_ref:
                return memory
            
            # 如果没有精确匹配，使用时间戳匹配
            diff = abs(memory["timestamp"] - timestamp)
            if diff <= tolerance and diff < best_diff:
                best_match = memory
                best_diff = diff
        
        return best_match

class AIPsychologist:
    """Main AI Psychologist class with long-term memory capabilities"""
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.llm_client = LLMClient()  # 使用统一的LLM客户端
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
    
    def _process_time_reference(self, user_message: str) -> Optional[str]:
        """处理用户消息中的时间参考"""
        time_ref = self.memory_system._extract_time_reference(user_message)
        if time_ref:
            # 检索相关情景记忆
            episodic_memory = self.memory_system.get_episodic_memory_by_time(time_ref)
            if episodic_memory:
                # 使用统一的数据结构处理
                try:
                    # 获取摘要信息
                    summary = episodic_memory.get("summary", "发生了某些事件")
                    activity = episodic_memory.get("activity", "进行了某些活动")
                    
                    return f"根据我们之前在{time_ref}的对话记录：{summary}"
                except Exception as e:
                    # 如果出现任何错误，打印错误信息并返回默认响应
                    print(f"处理时间参考时出错: {e}")
                    return None
        
        return None

    def _build_context(self, user_message: str) -> List[Dict[str, str]]:
        """Build context for the LLM using multi-layered memory"""
        # Start with working memory (recent conversation)
        context = self.memory_system.get_working_memory_context()
        
        # Add the main system prompt with current time
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        main_system_prompt = f"你是一位AI心理学家，运用你的专业知识解决用户的心理问题，必须遵守安全原则，现在的时间是{current_time}，你是具有长期记忆的（系统会给你）。"
        
        context.insert(0, {
            "role": "system",
            "content": main_system_prompt
        })
        
        # 检查是否有时间参考
        time_context = self._process_time_reference(user_message)
        if time_context:
            context.insert(1, {  # 插入到主系统提示之后
                "role": "system",
                "content": f"历史背景: {time_context}"
            })
        
        # Add relevant therapeutic techniques based on user message
        relevant_techniques = procedural_memory.get_relevant_techniques(user_message)
        if relevant_techniques:
            technique_info = "可用的治疗技术:\n"
            for name, technique in list(relevant_techniques.items())[:3]:  # Limit to 3 techniques
                technique_info += procedural_memory.format_technique_for_prompt(name, technique) + "\n"
            
            context.insert(1, {  # 插入到主系统提示之后
                "role": "system",
                "content": f"治疗技术参考:\n{technique_info}"
            })
        
        # Add relevant episodic memories
        relevant_memories = self.memory_system.get_relevant_episodic_memories(user_message)
        if relevant_memories:
            memory_summary = "相关的过往对话:\n"
            for mem in relevant_memories[-3:]:  # Last 3 memories
                # 使用统一的数据结构处理
                if "interaction" in mem:
                    # 新的统一结构
                    summary = mem.get("summary", "对话")
                else:
                    # 旧的结构或其他结构
                    summary = mem.get("summary", "对话")
                
                memory_summary += f"- {summary}\n"
            
            context.insert(1, {  # 插入到主系统提示之后
                "role": "system",
                "content": f"历史背景: {memory_summary}"
            })
        
        # Add user profile information
        user_profile = self.memory_system.get_user_profile()
        if user_profile:
            profile_info = f"用户档案: {json.dumps(user_profile, ensure_ascii=False)}"
            context.insert(1, {  # 插入到主系统提示之后
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
        
        # 检查用户是否提到特定时间点
        time_ref = self.memory_system._extract_time_reference(user_message)
        if time_ref:
            # 提取活动信息
            activity_info = {
                "user_message": user_message,
                "ai_response": ai_response,
                "emotional_insights": emotional_insights,
                "activity": self._extract_activity(user_message)
            }
            
            # 添加到基于时间的情景记忆
            self.memory_system.add_time_based_episodic_memory(time_ref, activity_info)
        else:
            # 添加到普通情景记忆
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

    def _extract_activity(self, user_message: str) -> str:
        """从用户消息中提取活动信息"""
        # 简单实现：基于关键词提取活动
        activities = {
            "实习": ["实习", "工作", "上班"],
            "学习": ["学习", "复习", "上课", "考试"],
            "旅行": ["旅行", "旅游", "游玩"],
            "休息": ["休息", "放松", "睡觉"],
            "运动": ["运动", "跑步", "健身"],
            "社交": ["聚会", "朋友", "聊天"]
        }
        
        user_message_lower = user_message.lower()
        for activity, keywords in activities.items():
            for keyword in keywords:
                if keyword in user_message_lower:
                    return activity
        
        return "其他活动"

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