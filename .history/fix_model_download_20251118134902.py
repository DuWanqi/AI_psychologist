#!/usr/bin/env python3
"""
修复模型下载问题的脚本
"""

import sys
import os
import subprocess

def check_model_cache():
    """检查模型缓存状态"""
    try:
        # 检查缓存目录
        cache_dirs = [
            os.path.expanduser("~/.cache/huggingface/"),
            os.path.expanduser("~/AppData/Local/huggingface/"),  # Windows
        ]
        
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        print(f"检查模型 '{model_name}' 的缓存状态...")
        
        found = False
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                model_path = os.path.join(cache_dir, "hub", model_name.replace("/", "--"))
                if os.path.exists(model_path):
                    print(f"✓ 在 {cache_dir} 找到模型缓存")
                    found = True
                    # 显示缓存大小
                    total_size = 0
                    for dirpath, dirnames, filenames in os.walk(model_path):
                        for f in filenames:
                            fp = os.path.join(dirpath, f)
                            total_size += os.path.getsize(fp)
                    print(f"  缓存大小: {total_size / (1024*1024):.1f} MB")
        
        if not found:
            print("⚠️  未找到模型缓存")
            return False
        return True
        
    except Exception as e:
        print(f"检查缓存时出错: {e}")
        return False

def setup_china_mirror():
    """设置国内镜像源"""
    print("设置国内镜像源...")
    print("请在命令行中运行以下命令:")
    print("set HF_ENDPOINT=https://hf-mirror.com")
    print("或者在Linux/macOS中:")
    print("export HF_ENDPOINT=https://hf-mirror.com")

def download_model_manual():
    """手动下载模型的说明"""
    print("手动下载模型说明:")
    print("1. 访问 https://hf-mirror.com/models/sentence-transformers/all-MiniLM-L6-v2")
    print("2. 下载模型文件")
    print("3. 将文件解压到缓存目录:")
    print("   Windows: %USERPROFILE%\\.cache\\huggingface\\hub\\")
    print("   Linux/macOS: ~/.cache/huggingface/hub/")

def test_model_loading():
    """测试模型加载"""
    print("测试模型加载...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ 模型加载成功")
        return True
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return False

def main():
    print("AI心理学家模型下载问题修复工具")
    print("=" * 40)
    
    # 检查模型缓存
    has_cache = check_model_cache()
    
    if not has_cache:
        print("\n检测到模型下载问题，提供以下解决方案:")
        print("1. 设置国内镜像源")
        print("2. 手动下载模型")
        print("3. 测试模型加载")
        
        choice = input("\n请选择解决方案 (1-3, 或 q 退出): ").strip()
        
        if choice == "1":
            setup_china_mirror()
        elif choice == "2":
            download_model_manual()
        elif choice == "3":
            test_model_loading()
        elif choice.lower() == "q":
            print("退出工具")
            return 0
        else:
            print("无效选择")
    
    print("\n建议:")
    print("1. 如果网络连接有问题，请检查防火墙设置")
    print("2. 如果在国内，建议使用国内镜像源")
    print("3. 可以尝试使用代理服务器")
    print("4. 重启应用程序测试是否解决问题")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())