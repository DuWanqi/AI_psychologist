#!/usr/bin/env python3
"""
测试修复后的时间参考记忆功能
"""

import sys
import os
import json

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_fix():
    """测试修复后的时间参考记忆功能"""
    try:
        # 导入必要的模块
        from ai_psychologist import AIPsychologist
        
        print("测试修复后的时间参考记忆功能")
        print("=" * 30)
        
        # 创建心理学家实例
        psychologist = AIPsychologist("test_fix_user")
        
        # 测试1: 用户提供时间参考信息
        print("测试1: 用户提供时间参考信息...")
        user_message = "我今年暑假，也就是2025年暑假做了3个月的实习。"
        response = psychologist.chat(user_message)
        print(f"用户: {user_message}")
        print(f"AI: {response}")
        
        # 测试2: 查询时间参考信息
        print("\n测试2: 查询时间参考信息...")
        query_message = "你还记得我今年暑假，也就是2025年暑假干了什么吗？"
        response = psychologist.chat(query_message)
        print(f"用户: {query_message}")
        print(f"AI: {response}")
        
        # 检查内存中是否有时间参考记录
        print(f"\n情景记忆条目数: {len(psychologist.memory_system.episodic_memory)}")
        if psychologist.memory_system.episodic_memory:
            print("最新情景记忆:")
            latest_memory = psychologist.memory_system.episodic_memory[-1]
            print(f"  时间参考: {latest_memory.get('time_reference', '无')}")
            print(f"  摘要: {latest_memory.get('summary', '无')}")
            print(f"  时间: {latest_memory.get('datetime', '无')}")
            print(f"  详情键存在: {'details' in latest_memory}")
        
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if test_fix():
        print("\n✅ 修复后的时间参考记忆测试完成!")
    else:
        print("\n❌ 修复后的时间参考记忆测试失败!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())