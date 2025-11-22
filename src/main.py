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
    parser.add_argument("--voice", action="store_true",
                       help="Enable voice input mode")
    parser.add_argument("--voice-model", type=str, default=None,
                       help="Path to Vosk voice model (e.g., models/vosk-model-small-cn-0.22)")
    
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
    
    # Initialize speech recognizer (if voice mode is enabled)
    speech_recognizer = None
    if args.voice:
        try:
            from speech_recognition import SpeechRecognition
            # Use specified model path or None for default
            model_path = args.voice_model if args.voice_model and os.path.exists(args.voice_model) else None
            speech_recognizer = SpeechRecognition(model_path)
            if model_path:
                print(f"语音输入模式已启用，使用模型: {model_path}")
            else:
                print("语音输入模式已启用，使用默认模型")
        except ImportError as e:
            print(f"语音识别模块导入失败: {e}")
            print("将使用文本输入模式")
            args.voice = False
        except Exception as e:
            print(f"语音识别初始化失败: {e}")
            print("将使用文本输入模式")
            args.voice = False
    
    try:
        while True:
            try:
                if args.voice and speech_recognizer:
                    print("\n按回车键开始语音输入（或输入'quit'退出）:")
                    user_input = input().strip()
                    
                    if user_input.lower() in ['quit', 'exit', '再见', '退出']:
                        break
                    
                    # Use speech recognition
                    user_input = speech_recognizer.recognize_from_microphone()
                    if user_input:
                        print(f"识别结果: {user_input}")
                    else:
                        print("未识别到语音，请重试")
                        continue
                else:
                    user_input = input("\nYou: ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', '再见', '退出']:
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
    finally:
        # Clean up resources
        if speech_recognizer:
            try:
                speech_recognizer.close()
            except:
                pass

if __name__ == "__main__":
    main()