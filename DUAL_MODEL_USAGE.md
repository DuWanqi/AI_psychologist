# 双模型支持使用说明

AI心理学家现在支持两种AI模型提供商，用户可以在运行时选择使用哪种模型：

## 支持的模型

1. **OpenRouter模型** (在线)
   - 默认模型: `tngtech/deepseek-r1t2-chimera:free`
   - 需要网络连接
   - 通过API调用

2. **Ollama模型** (本地)
   - 默认模型: `llama3.2:latest`
   - 完全本地运行
   - 无需网络连接

## 使用方法

### 1. 通过命令行参数指定模型

```bash
# 使用OpenRouter模型
python src/main.py --user-id patient_001 --model openrouter

# 使用Ollama模型
python src/main.py --user-id patient_001 --model ollama
```

### 2. 交互式选择模型

如果不指定`--model`参数，程序会提示用户选择：

```bash
python src/main.py --user-id patient_001
```

程序会显示：
```
请选择要使用的AI模型:
1. OpenRouter (在线模型)
2. Ollama (本地模型)
请输入选择 (1 或 2):
```

### 3. 通过环境变量配置

可以在`.env`文件中设置默认模型：

```env
# 选择模型提供商: openrouter 或 ollama
MODEL_PROVIDER=openrouter

# OpenRouter配置
OPENROUTER_API_KEY=your_api_key_here
DEFAULT_MODEL=tngtech/deepseek-r1t2-chimera:free

# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
```

## Ollama模型设置

### 1. 安装Ollama

访问 [Ollama官网](https://ollama.com/) 下载并安装Ollama。

### 2. 拉取模型

```bash
# 拉取Llama3.2 7B模型
ollama pull llama3.2:latest

# 或者拉取其他支持的模型
ollama pull llama3.1:8b
```

### 3. 启动Ollama服务

Ollama安装后会自动启动服务。可以通过以下命令验证：

```bash
ollama list
```

应该能看到类似输出：
```
NAME               ID              SIZE      MODIFIED
llama3.2:latest    a80c4f17acd5    2.0 GB    2 weeks ago
```

## 配置文件说明

### .env文件配置项

- `MODEL_PROVIDER`: 模型提供商 (openrouter 或 ollama)
- `OPENROUTER_API_KEY`: OpenRouter API密钥
- `DEFAULT_MODEL`: OpenRouter默认模型
- `OLLAMA_BASE_URL`: Ollama服务地址
- `OLLAMA_MODEL`: Ollama默认模型

## 性能和成本对比

### OpenRouter模型
- **优势**:
  - 通常提供更强的推理能力
  - 无需本地硬件资源
  - 模型更新及时
- **劣势**:
  - 需要网络连接
  - 可能有API调用成本
  - 数据需要通过网络传输

### Ollama模型
- **优势**:
  - 完全本地运行，隐私性好
  - 无API调用成本
  - 响应速度快（取决于本地硬件）
- **劣势**:
  - 需要本地硬件资源
  - 模型能力可能不如高端在线模型
  - 需要手动更新模型

## 硬件要求

### OpenRouter模型
- 任何能连接网络的设备
- 无需特殊硬件

### Ollama模型
- **最低配置**:
  - RAM: 16GB
  - CPU: 现代多核处理器
- **推荐配置**:
  - RAM: 32GB或更多
  - GPU: 支持CUDA的NVIDIA显卡（可选但推荐）
  - CPU: 高性能多核处理器

## 故障排除

### 1. Ollama服务未运行
```
Error: Connection refused
```
解决方案: 确保Ollama服务正在运行。

### 2. 模型未找到
```
Error: Model not found
```
解决方案: 使用`ollama pull`命令拉取所需模型。

### 3. 内存不足
```
Error: Out of memory
```
解决方案: 
- 关闭其他应用程序释放内存
- 使用量化版本的模型
- 升级硬件

## 测试双模型支持

可以运行测试脚本来验证双模型功能：

```bash
python test_dual_model.py
```

这将分别测试OpenRouter和Ollama模型的功能。