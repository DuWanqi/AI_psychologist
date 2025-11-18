#!/usr/bin/env python3
"""
统一记忆数据结构脚本
将所有现有的情景记忆文件转换为统一的数据结构
"""

import sys
import os
import json
from datetime import datetime

def unify_memory_structure():
    """统一记忆数据结构"""
    print("统一记忆数据结构")
    print("=" * 30)
    
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
            
            # 转换为统一的数据结构
            unified_count = 0
            for i, memory in enumerate(episodic_memories):
                # 检查是否需要转换
                needs_conversion = False
                
                # 如果有details字段，需要转换为统一结构
                if "details" in memory:
                    needs_conversion = True
                    # 转换details结构为统一的interaction结构
                    first_detail = memory["details"][0] if memory["details"] else {}
                    
                    # 创建统一结构
                    unified_memory = {
                        "id": memory.get("id", str(datetime.now().timestamp())),
                        "timestamp": memory.get("timestamp", datetime.now().timestamp()),
                        "datetime": memory.get("datetime", datetime.now().isoformat()),
                        "interaction": {
                            "user_message": first_detail.get("user_message", ""),
                            "ai_response": first_detail.get("ai_response", ""),
                            "emotional_insights": first_detail.get("emotional_insights", {})
                        },
                        "activity": first_detail.get("activity", "其他活动"),
                        "summary": memory.get("summary", "进行了某些活动")
                    }
                    
                    # 如果有时间参考，添加时间参考字段
                    if "time_reference" in memory:
                        unified_memory["time_reference"] = memory["time_reference"]
                    
                    # 替换原记忆条目
                    episodic_memories[i] = unified_memory
                    unified_count += 1
                
                # 如果有interaction但缺少某些字段，补充缺失字段
                elif "interaction" in memory:
                    # 确保所有必需字段都存在
                    if "activity" not in memory:
                        memory["activity"] = "其他活动"
                        unified_count += 1
                    
                    if "datetime" not in memory:
                        memory["datetime"] = datetime.fromtimestamp(memory.get("timestamp", datetime.now().timestamp())).isoformat()
                        unified_count += 1
            
            # 保存统一后的情景记忆
            if unified_count > 0:
                with open(episodic_file, 'w', encoding='utf-8') as f:
                    json.dump(episodic_memories, f, ensure_ascii=False, indent=2)
                print(f"  用户 {user_id}: 统一了 {unified_count} 个记忆条目")
            else:
                print(f"  用户 {user_id}: 无需统一")
        
        print("\n✅ 记忆数据结构统一完成!")
        return True
        
    except Exception as e:
        print(f"统一记忆数据结构时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("记忆数据结构统一工具")
    print("=" * 30)
    print("此工具将把所有情景记忆文件转换为统一的数据结构")
    print("统一后的结构将包含: id, timestamp, datetime, interaction, activity, summary")
    print("时间参考记忆还会包含: time_reference")
    
    response = input("\n是否继续? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("操作已取消")
        return 0
    
    if unify_memory_structure():
        print("\n🎉 记忆数据结构统一完成!")
        print("现在可以安全地删除旧的不兼容记忆文件了")
    else:
        print("\n❌ 记忆数据结构统一失败!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())