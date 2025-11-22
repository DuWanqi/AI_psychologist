# AI Psychologist with Long-Term Memory

An AI-powered mental health assistant with long-term memory capabilities, designed to provide empathetic psychological support while maintaining user privacy through local data storage.

## Features

### ✅ Core Features
- **Multi-layered Memory System**: Working memory, episodic memory, semantic memory, and procedural memory
- **Empathetic Conversations**: Three-stage empathy model (emotion recognition, empathetic expression, strategic support)
- **Personalized Interaction**: Customizable personality and communication style
- **Local Data Storage**: All data stored locally for privacy protection

### ✅ Memory Management
- **Hierarchical Memory Organization**: Structured memory layers based on human memory models
- **Memory Persistence**: Long-term storage using JSON files and vector databases
- **Intelligent Retrieval**: Context-aware memory recall for personalized responses

### ✅ Voice Interaction (New!)
- **Speech-to-Text**: Offline voice recognition using Vosk API
- **Privacy Protection**: All voice processing done locally without internet connection
- **Multilingual Support**: Supports Chinese and other languages

## Project Structure

```
AI_psychologist/
├── src/
│   ├── main.py              # Main application entry point
│   ├── ai_psychologist.py   # Core AI implementation
│   ├── config.py            # Configuration management
│   ├── procedural_memory.py # Therapeutic techniques management
│   └── speech_recognition.py # Voice input processing (New!)
├── requirements.txt         # Python dependencies
├── README.md               # Comprehensive documentation
├── requirements.md         # English requirements document
├── requirements_zh.md      # Chinese requirements document
├── proposal.txt            # Project proposal
├── 技术参考.txt             # Technical reference document
├── .env.example            # Environment variable template
├── run.ps1                 # Windows execution script
├── run.sh                  # Linux/macOS execution script
├── setup.ps1               # Windows setup script
├── setup.sh                # Linux/macOS setup script
├── demo.py                 # Demonstration script
└── test_installation.py    # Installation verification script
```

## Technology Stack

- **Language**: Python 3.8+
- **AI Integration**: OpenRouter API (with fallback to mock responses)
- **Memory Storage**: ChromaDB vector database (with file-based fallback)
- **Voice Recognition**: Vosk API (offline speech recognition)
- **Dependencies**: OpenAI, ChromaDB, sentence-transformers, python-dotenv, vosk, pyaudio

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd AI_psychologist
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Copy the example environment file and edit it with your OpenRouter API key:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

## Usage

### Running the Application

To start a conversation with the AI Psychologist:
```bash
python src/main.py --user-id your_user_id
```

To specify a user ID (for maintaining separate memory profiles):
```bash
python src/main.py --user-id your_user_id
```

To reset memory for a user:
```bash
python src/main.py --user-id your_user_id --reset-memory
```

To enable voice input mode:
```bash
python src/main.py --user-id your_user_id --voice
```

### During Conversation

- Type your messages naturally as you would in a conversation with a psychologist
- The system will remember important information from your conversations
- Type `quit`, `exit`, or `bye` to end the session

### Voice Input Mode

When using the `--voice` flag:

1. Press Enter to start voice input
2. Speak clearly when prompted
3. The system will transcribe your speech to text
4. The AI Psychologist will respond as usual

## Configuration

The application can be configured through environment variables in the `.env` file:

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required for real AI responses)
- `DATA_STORAGE_PATH`: Path to store user data (default: `./data`)
- `VECTOR_DB_PATH`: Path to store vector database (default: `./vector_db`)
- `DEFAULT_MODEL`: Default AI model to use (default: `openrouter/auto`)
- `WORKING_MEMORY_SIZE`: Number of recent messages to keep in working memory (default: 10)
- `EPISODIC_MEMORY_LIMIT`: Maximum number of episodic memories to store (default: 100)
- `THERAPEUTIC_TECHNIQUES_FILE`: Path to therapeutic techniques configuration (default: `./config/therapeutic_techniques.json`)

## Dependencies

- `openai`: For OpenRouter API integration
- `chromadb`: Vector database for semantic memory
- `sentence-transformers`: For generating text embeddings
- `python-dotenv`: For loading environment variables
- `vosk`: For offline speech recognition
- `pyaudio`: For audio input processing

## Future Enhancements

1. **Advanced Emotion Detection**: Integration with NLP libraries for better sentiment analysis
2. **Therapeutic Technique Integration**: Implementation of CBT, DBT, and other evidence-based methods
3. **Web Interface**: Development of a user-friendly web frontend
4. **Voice Interaction**: Speech-to-text and text-to-speech capabilities
5. **Multi-Language Support**: Expansion to support multiple languages

## Educational Value

This project demonstrates:
- Advanced AI application development
- Memory system design and implementation
- Privacy-preserving AI systems
- Modular software architecture
- Cross-platform deployment strategies

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenRouter for providing accessible AI models
- ChromaDB for vector database technology
- Vosk for offline speech recognition
- Sentence Transformers for embedding generation