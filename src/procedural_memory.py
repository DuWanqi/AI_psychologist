"""
程序性记忆模块 - 管理预设的治疗技术和案例
"""

import json
import os
from config import Config

class ProceduralMemory:
    """管理预设的治疗技术和案例库"""
    
    def __init__(self):
        """初始化程序性记忆"""
        self.techniques = {}
        self.load_therapeutic_techniques()
    
    def load_therapeutic_techniques(self):
        """加载预设的治疗技术"""
        try:
            # 确保配置文件存在
            if os.path.exists(Config.THERAPEUTIC_TECHNIQUES_FILE):
                with open(Config.THERAPEUTIC_TECHNIQUES_FILE, 'r', encoding='utf-8') as f:
                    self.techniques = json.load(f)
                print(f"✓ 成功加载 {len(self.techniques)} 个治疗技术")
            else:
                print(f"! 未找到治疗技术配置文件: {Config.THERAPEUTIC_TECHNIQUES_FILE}")
                self.techniques = {}
        except Exception as e:
            print(f"✗ 加载治疗技术时出错: {e}")
            self.techniques = {}
    
    def get_all_techniques(self):
        """获取所有治疗技术"""
        return self.techniques
    
    def get_technique(self, name):
        """根据名称获取特定治疗技术"""
        return self.techniques.get(name)
    
    def get_relevant_techniques(self, keywords):
        """根据关键词获取相关治疗技术"""
        relevant = {}
        keywords = keywords.lower()
        
        for name, technique in self.techniques.items():
            # 检查技术名称和描述是否包含关键词
            if (keywords in name.lower() or 
                keywords in technique.get('description', '').lower()):
                relevant[name] = technique
            
            # 检查步骤中是否包含关键词
            for step in technique.get('steps', []):
                if keywords in step.lower():
                    relevant[name] = technique
                    break
        
        return relevant
    
    def format_technique_for_prompt(self, name, technique):
        """将治疗技术格式化为提示词格式"""
        formatted = f"治疗技术: {name}\n"
        formatted += f"描述: {technique.get('description', '')}\n"
        formatted += "步骤:\n"
        for i, step in enumerate(technique.get('steps', []), 1):
            formatted += f"  {i}. {step}\n"
        
        formatted += "应用示例:\n"
        for example in technique.get('examples', [])[:2]:  # 限制示例数量
            formatted += f"  场景: {example.get('scenario', '')}\n"
            formatted += f"  回应: {example.get('response', '')}\n"
        
        return formatted

# 全局实例
procedural_memory = ProceduralMemory()