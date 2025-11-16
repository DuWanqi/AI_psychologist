#!/usr/bin/env python3
"""
修复情景记忆数据结构兼容性问题
"""

import sys
import os
import json

def fix_memory_compatibility():
    """修复情景记忆数据结构兼容性问题"""
    try:
        # 查找所有用户的数据目录
        data_dir = "./data"
        if not os.path.exists(data_dir):
            print("数据目录不存在")
            return True
            
        for user_id in os.listdir(data_dir):
            user_dir = os.path.join(data_dir, user_id)
            if not os.path.isdir(user_dir):
                continue
                
            episodic_file = os.path.join(user_dir, "episodic_memory.json")
            if not os.path.exists(episodic_file):
                continue
                
            print(f"处理用户 {user_id} 的情景记忆...")
            
            # 读取现有情景记忆
            with open(episodic_file, 'r', encoding='utf-8') as f:
                episodic_memories = json.load(f)
            
            # 检查并修复数据结构
            fixed_count = 0
            for i, memory in enumerate(episodic_memories):
                # 检查是否是旧的数据结构
                if "interaction" in memory and "details" not in memory:
                    # 转换为新的兼容结构
                    memory["details"] = [memory["interaction"]]
                    fixed_count += 1
                    print(f"  修复了记忆条目 {i+1}")
            
            # 保存修复后的情景记忆
            if fixed_count > 0:
                with open(episodic_file, 'w', encoding='utf-8') as f:
                    json.dump(episodic_memories, f, ensure_ascii=False, indent=2)
                print(f"  用户 {user_id}: 修复了 {fixed_count} 个记忆条目")
            else:
                print(f"  用户 {user_id}: 无需修复")
        
        print("\n✅ 情景记忆数据结构兼容性修复完成!")
        return True
        
    except Exception as e:
        print(f"修复失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("修复情景记忆数据结构兼容性问题")
    print("=" * 30)
    
    if fix_memory_compatibility():
        print("\n✅ 修复完成! 现在可以正常使用时间参考功能了。")
    else:
        print("\n❌ 修复失败!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())