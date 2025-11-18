#!/usr/bin/env python3
"""
Main entry point for the AI Psychologist application
"""

import argparse
import sys
import traceback
import os

# 导入模块
from ai_psychologist import AIPsychologist

def select_model_provider():
    """让用户选择模型提供商"""
    print("请选择要使用的AI模型:")
    print("1. OpenRouter (在线模型)")
    print("2. Ollama (本地模型)")
    
    while True:
        choice = input("请输入选择 (1 或 2): ").strip()
        if choice == "1":
            os.environ["MODEL_PROVIDER"] = "openrouter"
            print("已选择 OpenRouter 模型")
            break
        elif choice == "2":
            os.environ["MODEL_PROVIDER"] = "ollama"
            print("已选择 Ollama 本地模型")
            break
        else:
            print("无效选择，请输入 1 或 2")

def main():
    parser = argparse.ArgumentParser(description="AI Psychologist with Long-Term Memory")
    parser.add_argument("--user-id", required=True, help="User ID for memory isolation")
    parser.add_argument("--model", choices=["openrouter", "ollama"], 
                       help="Model provider to use (openrouter or ollama)")
    
    args = parser.parse_args()
    
    # 如果通过命令行参数指定了模型，则设置环境变量
    if args.model:
        os.environ["MODEL_PROVIDER"] = args.model
        print(f"使用命令行参数指定的模型: {args.model}")
    else:
        # 否则让用户选择模型
        select_model_provider()
    
    # 创建AI心理学家实例
    psychologist = AIPsychologist(args.user_id)
    
    # 显示当前使用的模型信息（从环境变量获取）
    model_provider = os.environ.get("MODEL_PROVIDER", "openrouter")
    model_info = "OpenRouter" if model_provider.lower() == "openrouter" else "Ollama"
    print(f"Welcome to the AI Psychologist (使用 {model_info} 模型). Type 'quit' to exit.")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '再见', '退出']:
                print("\nAI Psychologist: Take care! Feel free to come back anytime you need support.")
                break
            
            if user_input:
                response = psychologist.chat(user_input)
                print(f"\nAI Psychologist: {response}")
                
        except KeyboardInterrupt:
            print("\n\nAI Psychologist: Take care! Feel free to come back anytime you need support.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again or restart the application.")
            # 打印完整的错误堆栈以便调试
            traceback.print_exc()

if __name__ == "__main__":
    main()