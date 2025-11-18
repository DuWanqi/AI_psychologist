#!/usr/bin/env python3
"""
测试向量数据库初始化
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_vector_db_init():
    """测试向量数据库初始化"""
    print("测试向量数据库初始化...")
    
    try:
        # 导入必要的模块
        from ai_psychologist import AIPsychologist
        print("✓ 成功导入AIPsychologist")
        
        # 创建AI心理学家实例
        ai = AIPsychologist(user_id="test_user")
        print("✓ 成功创建AIPsychologist实例")
        
        # 检查向量数据库是否初始化成功
        if ai.collection is not None:
            print("✓ 向量数据库初始化成功")
            return True
        else:
            print("⚠️ 向量数据库未初始化或已降级")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("AI心理学家向量数据库测试")
    print("=" * 25)
    
    success = test_vector_db_init()
    
    if success:
        print("\n🎉 向量数据库测试成功！")
    else:
        print("\n❌ 向量数据库测试失败。")