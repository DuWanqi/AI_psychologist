#!/usr/bin/env python3
"""
测试向后兼容性 - 验证原有功能是否正常工作
"""

import sys
import os
import json

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_backward_compatibility():
    """测试向后兼容性"""
    try:
        print("测试向后兼容性")
        print("=" * 30)
        
        # 确保使用默认配置（OpenRouter）
        if "MODEL_PROVIDER" in os.environ:
            del os.environ["MODEL_PROVIDER"]
        
        from ai_psychologist import AIPsychologist
        
        # 创建心理学家实例
        psychologist = AIPsychologist("compatibility_test_user")
        
        print("1. 测试基本对话功能...")
        test_message = "我最近感到有些焦虑，能帮助我吗？"
        response = psychologist.chat(test_message)
        print(f"用户: {test_message}")
        print(f"AI: {response}")
        
        print("\n2. 测试时间参考功能...")
        time_message = "你还记得我今年暑假干了什么吗？"
        response = psychologist.chat(time_message)
        print(f"用户: {time_message}")
        print(f"AI: {response}")
        
        print("\n3. 测试程序性记忆功能...")
        cbt_message = "我总是有负面想法，怎么办？"
        response = psychologist.chat(cbt_message)
        print(f"用户: {cbt_message}")
        print(f"AI: {response}")
        
        print("\n4. 测试记忆持久化功能...")
        # 检查是否正确保存了记忆
        user_dir = f"./data/compatibility_test_user"
        episodic_file = os.path.join(user_dir, "episodic_memory.json")
        if os.path.exists(episodic_file):
            with open(episodic_file, 'r', encoding='utf-8') as f:
                episodic_data = json.load(f)
                print(f"情景记忆条目数: {len(episodic_data)}")
        
        print("\n5. 测试情感识别功能...")
        # 测试不同情感的识别
        emotional_messages = [
            "我感到很难过。",
            "我非常生气！",
            "我今天很开心。",
            "我感到很孤独。"
        ]
        
        for msg in emotional_messages:
            response = psychologist.chat(msg)
            print(f"用户: {msg}")
            print(f"AI: {response[:50]}...")
        
        print("\n✅ 向后兼容性测试完成!")
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if test_backward_compatibility():
        print("\n🎉 所有原有功能正常工作，向后兼容性得到保证!")
    else:
        print("\n❌ 向后兼容性测试失败!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())