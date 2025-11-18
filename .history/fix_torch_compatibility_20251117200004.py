#!/usr/bin/env python3
"""
修复PyTorch兼容性问题
"""

import subprocess
import sys

def check_versions():
    """检查当前版本"""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "show", "torch"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("当前PyTorch版本信息:")
            print(result.stdout)
        else:
            print("未安装PyTorch")
    except Exception as e:
        print(f"检查版本时出错: {e}")

def fix_torch_compatibility():
    """修复PyTorch兼容性问题"""
    print("修复PyTorch兼容性问题...")
    print("=" * 30)
    
    try:
        # 尝试更新PyTorch
        print("1. 尝试更新PyTorch...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", 
            "torch", "torchvision", "torchaudio"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyTorch更新成功")
        else:
            print("⚠️ PyTorch更新失败，尝试降级方案...")
            
            # 尝试安装兼容版本
            print("2. 安装兼容版本组合...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "torch==1.13.1", "sentence-transformers==2.2.2", "chromadb==0.4.22"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 兼容版本安装成功")
            else:
                print("❌ 兼容版本安装失败")
                print("错误信息:")
                print(result.stderr)
                return False
                
        return True
        
    except Exception as e:
        print(f"修复过程中出错: {e}")
        return False

def main():
    print("PyTorch兼容性修复工具")
    print("=" * 30)
    
    # 检查当前版本
    check_versions()
    
    # 修复兼容性问题
    if fix_torch_compatibility():
        print("\n🎉 PyTorch兼容性问题修复完成!")
        print("请重新运行您的应用程序。")
    else:
        print("\n❌ PyTorch兼容性问题修复失败!")
        print("建议手动安装兼容版本:")
        print("pip install torch==1.13.1 sentence-transformers==2.2.2 chromadb==0.4.22")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())