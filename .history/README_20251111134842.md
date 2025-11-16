# AI Psychologist - An Empathetic Mental Health Chatbot with Long-Term Memory

## Overview

The AI Psychologist is an intelligent mental health assistant that provides personalized psychological support with long-term memory capabilities. The system remembers user psychological profiles, preferences, and consultation history to provide continuous and tailored support.

## Features

- **Multi-layered Memory System**: Implements working memory, episodic memory, semantic memory, and external persistent memory
- **Empathetic Conversations**: Uses a three-stage empathy model (emotion recognition, empathetic expression, strategic support)
- **Privacy-Focused**: All data is stored locally with no external transmission
- **Cost-Effective**: Utilizes OpenRouter's free tier models
- **Customizable Personality**: Multiple personality options for the AI psychologist

## Project Structure

```
AI_psychologist/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   ├── ai_psychologist.py   # Core AI psychologist implementation
│   └── config.py            # Configuration settings
├── data/                    # User data storage (created on first run)
├── vector_db/               # Vector database for semantic memory (created on first run)
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
├── README.md                # This file
├── requirements_zh.md       # Chinese requirements document
├── proposal.txt             # Project proposal
└── 技术参考.txt              # Technical reference document
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

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
python src/main.py
```

To specify a user ID (for maintaining separate memory profiles):
```bash
python src/main.py --user-id your_user_id
```

To reset memory for a user:
```bash
python src/main.py --user-id your_user_id --reset-memory
```

### During Conversation

- Type your messages naturally as you would in a conversation with a psychologist
- The system will remember important information from your conversations
- Type `quit`, `exit`, or `bye` to end the session

## Configuration

The application can be configured through environment variables in the `.env` file:

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required for real AI responses)
- `DATA_STORAGE_PATH`: Path for storing user data (default: `./data`)
- `VECTOR_DB_PATH`: Path for vector database storage (default: `./vector_db`)
- `DEFAULT_MODEL`: Default model to use (default: `openrouter/auto`)
- `WORKING_MEMORY_SIZE`: Number of recent messages to keep in working memory (default: `10`)
- `EPISODIC_MEMORY_LIMIT`: Maximum number of episodic memories to store (default: `100`)

## Memory System

The AI Psychologist implements a five-layer memory system based on human memory models:

1. **Working Memory**: Short-term conversation context (last N messages)
2. **Episodic Memory**: Time-stamped events and conversation history
3. **Semantic Memory**: Facts, knowledge, and user profiles
4. **Procedural Memory**: Therapeutic techniques and skills
5. **External Persistent Memory**: Long-term storage beyond session context

## Development

### Running the Demo

The application includes a demo mode that works without an API key. When no API key is provided, the system will use mock responses based on keyword detection.

### Extending Functionality

Key areas for extension:
- Enhanced emotion detection using NLP libraries
- Integration with more sophisticated psychological knowledge bases
- Implementation of specific therapeutic techniques (CBT, DBT, etc.)
- Web interface development
- Voice interaction capabilities

## Dependencies

- `openai`: For OpenRouter API integration
- `chromadb`: Vector database for semantic memory
- `numpy`: Numerical computing
- `sentence-transformers`: For generating embeddings
- `python-dotenv`: Environment variable management
- `tqdm`: Progress bars

## Privacy and Security

- All data is stored locally on the user's device
- No personal information is transmitted to external servers
- User data is stored in plain JSON files in the `data/` directory
- Memory files can be manually deleted for complete data removal

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure you have a valid OpenRouter API key in your `.env` file
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Memory Issues**: If experiencing memory problems, try resetting user memory with the `--reset-memory` flag

### Getting Help

If you encounter issues not covered in this README, please check the issue tracker or contact the development team.

## License

This project is for educational and research purposes. It is not intended to replace professional mental health services.

## Disclaimer

This AI Psychologist is not a licensed therapist and should not be used as a substitute for professional mental health care. If you are experiencing a mental health emergency, please contact emergency services or a crisis helpline immediately.