#!/usr/bin/env python3
"""
测试离线模式加载模型
"""

import os
import sys

def test_offline_model_loading():
    """测试离线模式加载模型"""
    print("测试离线模式加载SentenceTransformer模型...")
    
    # 设置离线模式
    os.environ['HF_HUB_OFFLINE'] = '1'
    print("✓ 已设置离线模式")
    
    try:
        # 导入必要的库
        from sentence_transformers import SentenceTransformer
        print("✓ 成功导入SentenceTransformer")
        
        # 尝试加载模型
        print("正在加载模型 'all-MiniLM-L6-v2'...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ 模型加载成功!")
        
        # 测试模型功能
        print("测试模型编码功能...")
        sentences = ["这是一个测试句子", "这是另一个测试句子"]
        embeddings = model.encode(sentences)
        print(f"✓ 编码成功，生成了 {len(embeddings)} 个向量，每个向量维度: {len(embeddings[0])}")
        
        return True
        
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        print("\n可能的解决方案:")
        print("1. 确保模型已下载并缓存")
        print("2. 检查缓存目录权限")
        print("3. 尝试重新下载模型:")
        print("   - 设置环境变量: set HF_ENDPOINT=https://hf-mirror.com")
        print("   - 然后重新运行此脚本")
        return False

def check_cache_status():
    """检查缓存状态"""
    print("检查模型缓存状态...")
    
    # 检查缓存目录
    cache_dirs = [
        os.path.expanduser("~/AppData/Local/huggingface/"),
        os.path.expanduser("~/.cache/huggingface/"),
    ]
    
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    
    found = False
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            # 检查hub目录
            hub_dir = os.path.join(cache_dir, "hub")
            if os.path.exists(hub_dir):
                # 查找模型目录
                for item in os.listdir(hub_dir):
                    if "all-MiniLM-L6-v2" in item:
                        model_path = os.path.join(hub_dir, item)
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
    
    return found

if __name__ == "__main__":
    print("AI心理学家离线模型测试工具")
    print("=" * 30)
    
    # 检查缓存
    has_cache = check_cache_status()
    
    if has_cache:
        # 测试离线加载
        success = test_offline_model_loading()
        if success:
            print("\n🎉 离线模式测试成功！")
            print("您的模型可以在没有网络连接的情况下正常工作。")
        else:
            print("\n❌ 离线模式测试失败。")
            print("请检查上述错误信息并尝试解决方案。")
    else:
        print("\n⚠️  未找到模型缓存，请先下载模型:")
        print("1. 设置环境变量: set HF_ENDPOINT=https://hf-mirror.com")
        print("2. 运行应用让模型自动下载")
        print("3. 或手动下载模型文件")