#!/usr/bin/env python3
"""
测试增强的语义记忆功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_enhanced_memory():
    """测试增强的语义记忆功能"""
    print("测试增强的语义记忆功能...")
    
    try:
        # 导入必要的模块
        from ai_psychologist import AIPsychologist
        print("✓ 成功导入AIPsychologist")
        
        # 创建AI心理学家实例
        ai = AIPsychologist(user_id="enhanced_test_user")
        print("✓ 成功创建AIPsychologist实例")
        
        # 测试对话来触发语义记忆更新
        test_messages = [
            "我最近在准备一个重要的工作面试，感到很焦虑。",
            "我喜欢在晚上和你聊天，因为那时候比较安静。",
            "我对学习新技能很感兴趣，特别是编程。",
            "最近睡眠不太好，经常失眠。",
        ]
        
        print("\n开始测试对话...")
        for i, message in enumerate(test_messages, 1):
            print(f"  {i}. 用户: {message}")
            response = ai.chat(message)
            print(f"     AI: {response[:50]}...")
        
        # 检查语义记忆更新
        user_profile = ai.memory_system.get_user_profile()
        print("\n语义记忆内容:")
        print(f"  用户档案: {user_profile}")
        
        # 检查具体的记忆内容
        preferences = user_profile.get("preferences", {})
        print(f"  偏好设置: {preferences}")
        
        personality_insights = user_profile.get("personality_insights", {})
        print(f"  个性洞察: {personality_insights}")
        
        psychological_history = user_profile.get("psychological_history", [])
        print(f"  心理历史: {len(psychological_history)} 条记录")
        
        # 检查向量数据库
        if hasattr(ai.memory_system, 'collection') and ai.memory_system.collection is not None:
            print("✓ 向量数据库已初始化")
        else:
            print("⚠️ 向量数据库未初始化或已降级")
            
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("AI心理学家增强语义记忆测试")
    print("=" * 30)
    
    success = test_enhanced_memory()
    
    if success:
        print("\n🎉 增强语义记忆测试成功！")
    else:
        print("\n❌ 增强语义记忆测试失败。")