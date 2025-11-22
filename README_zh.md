# AI心理学家 - 具有长期记忆的心理健康助手

一个具有长期记忆功能的AI心理健康助手，旨在提供富有同理心的心理支持，同时通过本地数据存储保护用户隐私。

## 功能特性

### ✅ 核心功能
- **多层记忆系统**：工作记忆、情景记忆、语义记忆和程序性记忆
- **共情对话**：三阶段共情模型（情绪识别、共情表达、策略性支持）
- **个性化交互**：可定制的人格和沟通风格
- **本地数据存储**：所有数据本地存储以保护隐私

### ✅ 记忆管理
- **分层记忆组织**：基于人类记忆模型的结构化记忆层
- **记忆持久化**：使用JSON文件和向量数据库进行长期存储
- **智能检索**：基于上下文的记忆调用以实现个性化响应

### ✅ 语音交互（新增！）
- **语音转文本**：使用Vosk API进行离线语音识别
- **隐私保护**：所有语音处理都在本地进行，无需网络连接
- **多语言支持**：支持中文等多种语言

## 项目结构

```
AI_psychologist/
├── src/
│   ├── main.py              # 主应用程序入口点
│   ├── ai_psychologist.py   # 核心AI实现
│   ├── config.py            # 配置管理
│   ├── procedural_memory.py # 治疗技术管理
│   └── speech_recognition.py # 语音输入处理（新增！）
├── requirements.txt         # Python依赖
├── README.md               # 英文综合文档
├── requirements.md         # 英文需求文档
├── requirements_zh.md      # 中文需求文档
├── proposal.txt            # 项目提案
├── 技术参考.txt             # 技术参考文档
├── .env.example            # 环境变量模板
├── run.ps1                 # Windows执行脚本
├── run.sh                  # Linux/macOS执行脚本
├── setup.ps1               # Windows设置脚本
├── setup.sh                # Linux/macOS设置脚本
├── demo.py                 # 演示脚本
└── test_installation.py    # 安装验证脚本
```

## 技术栈

- **语言**：Python 3.8+
- **AI集成**：OpenRouter API（带模拟响应的后备方案）
- **记忆存储**：ChromaDB向量数据库（带基于文件的后备方案）
- **语音识别**：Vosk API（离线语音识别）
- **依赖**：OpenAI, ChromaDB, sentence-transformers, python-dotenv, vosk, pyaudio

## 安装说明

### 先决条件

- Python 3.8或更高版本
- pip（Python包管理器）

### 安装步骤

1. **克隆或下载代码库**
   ```bash
   git clone <repository-url>
   cd AI_psychologist
   ```

2. **创建虚拟环境（推荐）**
   ```bash
   python -m venv venv
   # Windows系统
   venv\Scripts\activate
   # macOS/Linux系统
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **设置环境变量**
   复制示例环境文件并编辑以添加您的OpenRouter API密钥：
   ```bash
   cp .env.example .env
   ```
   然后编辑`.env`文件，添加您的OpenRouter API密钥：
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

## 使用方法

### 运行应用程序

启动与AI心理学家的对话：
```bash
python src/main.py --user-id your_user_id
```

指定用户ID（用于维护独立的记忆档案）：
```bash
python src/main.py --user-id your_user_id
```

重置用户的记忆：
```bash
python src/main.py --user-id your_user_id --reset-memory
```

启用语音输入模式：
```bash
python src/main.py --user-id your_user_id --voice
```

### 对话过程中

- 像与心理学家对话一样自然地输入消息
- 系统将记住您对话中的重要信息
- 输入`quit`、`exit`或`bye`结束会话

### 语音输入模式

使用`--voice`标志时：

1. 按回车键开始语音输入
2. 在提示时清晰地说话
3. 系统会将您的语音转录为文本
4. AI心理学家会像平常一样回应

## 配置说明

应用程序可以通过`.env`文件中的环境变量进行配置：

- `OPENROUTER_API_KEY`：您的OpenRouter API密钥（用于真实的AI响应）
- `DATA_STORAGE_PATH`：存储用户数据的路径（默认：`./data`）
- `VECTOR_DB_PATH`：存储向量数据库的路径（默认：`./vector_db`）
- `DEFAULT_MODEL`：要使用的默认AI模型（默认：`openrouter/auto`）
- `WORKING_MEMORY_SIZE`：工作记忆中保留的最近消息数（默认：10）
- `EPISODIC_MEMORY_LIMIT`：存储的情景记忆最大数量（默认：100）
- `THERAPEUTIC_TECHNIQUES_FILE`：治疗技术配置的路径（默认：`./config/therapeutic_techniques.json`）

## 依赖说明

- `openai`：用于OpenRouter API集成
- `chromadb`：用于语义记忆的向量数据库
- `sentence-transformers`：用于生成文本嵌入
- `python-dotenv`：用于加载环境变量
- `vosk`：用于离线语音识别
- `pyaudio`：用于音频输入处理

## 可扩展功能

1. **高级情绪检测**：集成NLP库以实现更好的情感分析
2. **治疗技术集成**：实现CBT、DBT等基于证据的方法
3. **Web界面**：开发用户友好的Web前端
4. **语音交互**：语音转文本和文本转语音功能
5. **多语言支持**：扩展以支持多种语言

## 教育价值

本项目展示了：
- 高级AI应用开发
- 记忆系统设计与实现
- 隐私保护的AI系统
- 模块化软件架构
- 跨平台部署策略

## 许可证

本项目采用MIT许可证 - 详见LICENSE文件了解详情。

## 致谢

- OpenRouter提供可访问的AI模型
- ChromaDB提供向量数据库技术
- Vosk提供离线语音识别
- Sentence Transformers提供嵌入生成