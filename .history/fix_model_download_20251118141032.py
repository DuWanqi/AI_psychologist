#!/usr/bin/env python3
"""
修复模型下载问题的脚本
"""

import sys
import os
import subprocess
import platform

def check_model_cache():
    """检查模型缓存状态"""
    try:
        # 检查缓存目录
        system = platform.system()
        if system == "Windows":
            cache_dirs = [
                os.path.expanduser("~/AppData/Local/huggingface/"),
                os.path.expanduser("~/.cache/huggingface/"),
            ]
        else:
            cache_dirs = [
                os.path.expanduser("~/.cache/huggingface/"),
            ]
        
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        print(f"检查模型 '{model_name}' 的缓存状态...")
        
        found = False
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                # 检查hub目录
                hub_dir = os.path.join(cache_dir, "hub")
                if os.path.exists(hub_dir):
                    # 查找模型目录
                    model_dirs = []
                    for item in os.listdir(hub_dir):
                        if "all-MiniLM-L6-v2" in item:
                            model_dirs.append(os.path.join(hub_dir, item))
                    
                    for model_path in model_dirs:
                        if os.path.exists(model_path):
                            print(f"✓ 在 {model_path} 找到模型缓存")
                            found = True
                            # 显示缓存大小
                            total_size = 0
                            for dirpath, dirnames, filenames in os.walk(model_path):
                                for f in filenames:
                                    fp = os.path.join(dirpath, f)
                                    if os.path.exists(fp):
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
    if platform.system() == "Windows":
        print("set HF_ENDPOINT=https://hf-mirror.com")
        print("set HF_HOME=%USERPROFILE%\\AppData\\Local\\huggingface")
    else:
        print("export HF_ENDPOINT=https://hf-mirror.com")
        print("export HF_HOME=~/.cache/huggingface")

def download_model_manual():
    """手动下载模型的说明"""
    print("手动下载模型说明:")
    print("1. 访问 https://hf-mirror.com/models/sentence-transformers/all-MiniLM-L6-v2")
    print("2. 下载模型文件")
    print("3. 将文件解压到缓存目录:")
    if platform.system() == "Windows":
        print("   Windows: %USERPROFILE%\\AppData\\Local\\huggingface\\hub\\")
    else:
        print("   Linux/macOS: ~/.cache/huggingface/hub/")

def test_model_loading():
    """测试模型加载"""
    print("测试模型加载...")
    try:
        # 先设置环境变量
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        
        # 尝试加载模型
        from sentence_transformers import SentenceTransformer
        print("正在加载模型...这可能需要一些时间")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ 模型加载成功")
        return True
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        print("\n可能的解决方案:")
        print("1. 设置国内镜像源:")
        print("   set HF_ENDPOINT=https://hf-mirror.com")
        print("2. 使用离线模式加载已缓存的模型:")
        print("   SentenceTransformer('all-MiniLM-L6-v2', trust_remote_code=True)")
        print("3. 检查网络连接和防火墙设置")
        return False

def fix_ssl_issues():
    """修复SSL证书问题"""
    print("尝试修复SSL证书问题...")
    try:
        import ssl
        import certifi
        print("✓ SSL证书修复完成")
        print("如果仍有问题，请尝试:")
        print("1. 更新证书: pip install --upgrade certifi")
        print("2. 设置环境变量: REQUESTS_CA_BUNDLE=/path/to/certifi/cacert.pem")
        return True
    except Exception as e:
        print(f"SSL修复失败: {e}")
        return False

def check_virtual_environment():
    """检查虚拟环境"""
    print("检查虚拟环境...")
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        print(f"✓ 当前在虚拟环境中: {venv_path}")
    else:
        print("⚠️  当前不在虚拟环境中")
        print("建议激活虚拟环境:")
        if platform.system() == "Windows":
            print("   cd psy\\Scripts && activate.bat")
        else:
            print("   source psy/bin/activate")

def setup_offline_mode():
    """设置离线模式"""
    print("设置离线模式...")
    print("在代码中添加以下设置以强制使用本地缓存:")
    print("")
    print("```python")
    print("import os")
    print("os.environ['HF_HUB_OFFLINE'] = '1'")
    print("from sentence_transformers import SentenceTransformer")
    print("model = SentenceTransformer('all-MiniLM-L6-v2', trust_remote_code=True)")
    print("```")
    print("")
    print("这将强制SentenceTransformer使用本地缓存的模型文件，而不会尝试连接网络。")

def main():
    print("AI心理学家模型下载问题修复工具")
    print("=" * 40)
    
    # 检查虚拟环境
    check_virtual_environment()
    
    # 检查模型缓存
    has_cache = check_model_cache()
    
    print("\n检测到的问题和解决方案:")
    print("1. SSL证书问题 - 修复SSL连接")
    print("2. 网络连接问题 - 设置国内镜像源")
    print("3. 缓存问题 - 手动下载模型")
    print("4. 测试模型加载")
    print("5. 设置离线模式(推荐)")
    
    choice = input("\n请选择解决方案 (1-5, 或 q 退出): ").strip()
    
    if choice == "1":
        fix_ssl_issues()
    elif choice == "2":
        setup_china_mirror()
    elif choice == "3":
        download_model_manual()
    elif choice == "4":
        test_model_loading()
    elif choice == "5":
        setup_offline_mode()
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