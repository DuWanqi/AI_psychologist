#!/usr/bin/env python3
"""
测试程序性记忆系统
"""

import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_procedural_memory():
    """测试程序性记忆系统"""
    try:
        from procedural_memory import procedural_memory
        
        print("程序性记忆系统测试")
        print("=" * 30)
        
        # 测试加载治疗技术
        techniques = procedural_memory.get_all_techniques()
        print(f"✓ 成功加载 {len(techniques)} 个治疗技术")
        
        # 显示所有治疗技术名称
        print("\n可用的治疗技术:")
        for name in techniques.keys():
            print(f"  - {name}")
        
        # 测试获取特定技术
        cbt = procedural_memory.get_technique("认知行为疗法")
        if cbt:
            print(f"\n✓ 成功获取认知行为疗法技术")
            print(f"  描述: {cbt['description']}")
            print(f"  步骤数量: {len(cbt['steps'])}")
        
        # 测试关键词搜索
        anxiety_techniques = procedural_memory.get_relevant_techniques("焦虑")
        print(f"\n✓ 关键词'焦虑'相关的技术数量: {len(anxiety_techniques)}")
        
        # 测试格式化输出
        if cbt:
            formatted = procedural_memory.format_technique_for_prompt("认知行为疗法", cbt)
            print(f"\n格式化输出示例 (前200字符):")
            print(formatted[:200] + "..." if len(formatted) > 200 else formatted)
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("程序性记忆系统测试脚本")
    print("=" * 25)
    
    if test_procedural_memory():
        print("\n✅ 程序性记忆系统测试通过!")
        print("\n使用方法:")
        print("1. 修改 ./config/therapeutic_techniques.json 文件添加新的治疗技术")
        print("2. 系统会自动加载这些预设的治疗技术")
        print("3. 在对话中，相关技术会自动提供给AI作为参考")
    else:
        print("\n❌ 程序性记忆系统测试失败!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())