#!/usr/bin/env python3
"""
测试记忆持久化功能
"""

import sys
import os
import json

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_memory_persistence():
    """测试记忆持久化"""
    try:
        # 导入必要的模块
        from ai_psychologist import AIPsychologist
        
        print("测试记忆持久化功能")
        print("=" * 30)
        
        # 创建心理学家实例
        psychologist = AIPsychologist("test_persistence")
        
        # 进行一次对话
        print("进行测试对话...")
        user_message = "我今年暑假计划去旅行，想去看看大海。"
        response = psychologist.chat(user_message)
        print(f"用户: {user_message}")
        print(f"AI: {response}")
        
        # 检查内存中是否有记录
        print(f"\n情景记忆条目数: {len(psychologist.memory_system.episodic_memory)}")
        if psychologist.memory_system.episodic_memory:
            print("最新情景记忆:")
            latest_memory = psychologist.memory_system.episodic_memory[-1]
            print(f"  摘要: {latest_memory.get('summary', '无')}")
            print(f"  时间: {latest_memory.get('datetime', '无')}")
        
        # 检查文件是否创建
        user_dir = f"./data/test_persistence"
        semantic_file = os.path.join(user_dir, "semantic_memory.json")
        episodic_file = os.path.join(user_dir, "episodic_memory.json")
        
        print(f"\n检查文件存储:")
        print(f"语义记忆文件存在: {os.path.exists(semantic_file)}")
        print(f"情景记忆文件存在: {os.path.exists(episodic_file)}")
        
        if os.path.exists(episodic_file):
            with open(episodic_file, 'r', encoding='utf-8') as f:
                episodic_data = json.load(f)
                print(f"情景记忆文件条目数: {len(episodic_data)}")
                if episodic_data:
                    print("文件中的最新记忆:")
                    latest = episodic_data[-1]
                    print(f"  摘要: {latest.get('summary', '无')}")
        
        # 创建新的实例测试持久化
        print("\n" + "=" * 30)
        print("创建新实例测试持久化...")
        new_psychologist = AIPsychologist("test_persistence")
        print(f"加载的情景记忆条目数: {len(new_psychologist.memory_system.episodic_memory)}")
        
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if test_memory_persistence():
        print("\n✅ 记忆持久化测试完成!")
    else:
        print("\n❌ 记忆持久化测试失败!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())