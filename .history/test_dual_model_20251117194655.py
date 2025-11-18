#!/usr/bin/env python3
"""
测试双模型支持功能
"""

import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_dual_model_support():
    """测试双模型支持功能"""
    try:
        print("测试双模型支持功能")
        print("=" * 30)
        
        # 测试OpenRouter模型
        print("1. 测试OpenRouter模型...")
        os.environ["MODEL_PROVIDER"] = "openrouter"
        
        from ai_psychologist import AIPsychologist
        psychologist = AIPsychologist("test_dual_model_user")
        
        test_message = "我最近感到有些焦虑，能帮助我吗？"
        response = psychologist.chat(test_message)
        print(f"用户: {test_message}")
        print(f"AI (OpenRouter): {response}")
        
        # 测试Ollama模型
        print("\n2. 测试Ollama模型...")
        os.environ["MODEL_PROVIDER"] = "ollama"
        
        # 重新创建实例以使用新模型
        psychologist_ollama = AIPsychologist("test_dual_model_user_ollama")
        
        response = psychologist_ollama.chat(test_message)
        print(f"用户: {test_message}")
        print(f"AI (Ollama): {response}")
        
        print("\n✅ 双模型支持测试完成!")
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if test_dual_model_support():
        print("\n🎉 双模型支持功能正常工作!")
    else:
        print("\n❌ 双模型支持测试失败!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())