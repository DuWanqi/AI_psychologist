#!/usr/bin/env python3
"""
简单的向量数据库测试
"""

import os
import sys

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_simple():
    print("开始测试...")
    
    # 设置离线模式
    os.environ['HF_HUB_OFFLINE'] = '1'
    print("已设置离线模式")
    
    # 测试直接导入和使用
    try:
        from ai_psychologist import AIPsychologist
        print("✓ 导入成功")
        
        # 创建实例
        ai = AIPsychologist(user_id="test_user")
        print("✓ 创建实例成功")
        
        # 检查内存系统
        if hasattr(ai, 'memory_system'):
            print("✓ 访问内存系统成功")
            memory_system = ai.memory_system
            
            # 检查collection
            if hasattr(memory_system, 'collection'):
                if memory_system.collection is not None:
                    print("✓ 向量数据库初始化成功")
                else:
                    print("⚠️ 向量数据库未初始化或已降级")
            else:
                print("❌ MemorySystem没有collection属性")
        else:
            print("❌ 没有memory_system属性")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()