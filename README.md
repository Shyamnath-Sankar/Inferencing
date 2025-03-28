# AI Text Generation System

A modular system for text generation using multiple AI providers with automatic API key rotation.

## Features

- 🔄 Automatic API key rotation
- 🔌 Dynamic provider integration
- 🌐 Clean architecture with separation of concerns
- 🚀 Real-time streaming responses
- 📝 Markdown rendering support
- 🛠 Easy provider integration

## System Architecture

The system follows a clean architecture pattern with these components:

### Backend (`/backend`)

- `core/` - Core system components
  - `config.py` - Configuration settings
  - `exceptions.py` - Error handling
  - `key_manager.py` - API key management
  - `text_generation.py` - Core business logic

- `models/` - Provider-specific implementations
  - `gemini.py` - Google Gemini implementation
  - `groq.py` - Groq implementation
  - `cohere.py` - Cohere implementation
  - etc.

### Frontend (`/frontend`)
- `index.html` - Web interface with streaming support

## Setup

1. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Configure API keys in `backend/apikeys.csv`:
```csv
GROQ API ,GEMINI API,COHERE  AI,Samba api key
key1,key1,key1,key1
key2,key2,key2,key2
...
```

3. Configure models in `backend/MODELS.csv`:
```csv
GROQ MODELS,COHERE,SambaNova,GEMINI
model1,model1,model1,model1
model2,model2,model2,model2
...
```

4. Start the server:
```bash
python backend/app.py
```

5. Access the web interface at:
```
http://localhost:8000/static/index.html
```

## Adding a New Provider

1. Add provider column to `MODELS.csv`:
```csv
GROQ MODELS,COHERE,NEW_PROVIDER
model1,model1,new-model-1
model2,model2,new-model-2
```

2. Add API keys to `apikeys.csv`:
```csv
GROQ API ,COHERE  AI,NEW_PROVIDER API
key1,key1,new-key-1
key2,key2,new-key-2
```

3. Create provider implementation in `backend/models/`:
```python
# backend/models/new_provider.py

async def run_model_stream(api_key: str, model: str, prompt: str):
    """
    Implement streaming response for the new provider.
    
    Args:
        api_key: The API key to use
        model: Model identifier
        prompt: User input prompt
        
    Yields:
        str: Generated text chunks
    """
    try:
        # Provider-specific implementation
        async for chunk in your_implementation():
            yield chunk
    except Exception as e:
        raise Exception(f"Error with provider: {str(e)}")
```

4. Restart the server - the system will automatically:
   - Detect the new provider
   - Load its models
   - Set up API key rotation
   - Make it available in the UI

## API Endpoints

- `GET /models` - List available models
- `POST /generate` - Generate text with streaming response
  ```json
  {
    "model": "model-name",
    "prompt": "Your prompt here"
  }
  ```

## Error Handling

The system includes comprehensive error handling:
- API key validation
- Model availability checks
- Provider module validation
- Request validation
- Streaming error handling

## Monitoring

Monitor API key rotation and usage through server logs:
```
[INFO] Using key #1/5 (AIza...22_o)
[INFO] Next request will use key #2/5
```

## License

MIT License