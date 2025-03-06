# AI Model Interface

A web application that allows users to select AI models from different providers and generate responses using rotating API keys.

## Project Structure

```
.
├── backend/
│   ├── models/
│   │   ├── cohere-test.py
│   │   ├── gemini.py
│   │   ├── groq.py
│   │   ├── mistral.py
│   │   └── sambanova.py
│   ├── MODELS.csv
│   ├── apikeys.csv
│   ├── app.py
│   ├── utils.py
│   └── requirements.txt
└── frontend/
    └── index.html
```

## Setup Instructions

1. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Run the backend server:
   ```bash
   cd backend
   uvicorn app:app --reload
   ```

3. Open the frontend:
   - Open `frontend/index.html` in a web browser
   - The interface will automatically connect to the backend running on http://localhost:8000

## How It Works

1. The application reads model information from `MODELS.csv` and API keys from `apikeys.csv`
2. The frontend displays available models in a dropdown menu
3. Users can select a model and enter a prompt
4. The backend automatically:
   - Determines the appropriate provider for the selected model
   - Rotates through available API keys for that provider
   - Calls the corresponding provider module to generate the response
   - Returns the response to the frontend

## Features

- Model selection from multiple providers (GROQ, Cohere, SambaNova, Gemini)
- Automatic API key rotation for each provider
- Simple and intuitive user interface
- Error handling and loading states
- Cross-Origin Resource Sharing (CORS) enabled

## CSV File Formats

### MODELS.csv
- Headers: Provider names (e.g., GROQ MODELS, COHERE, SambaNova, GEMINI)
- Rows: Model names available for each provider

### apikeys.csv
- Headers: Provider names with "API" suffix (e.g., GROQ API, GEMINI API)
- Rows: API keys for each provider (rotates through these keys)

## Error Handling

The application includes comprehensive error handling for:
- Missing or invalid API keys
- Invalid model selections
- API request failures
- Network errors

## Development

- Backend uses FastAPI for the API server
- Frontend is a simple HTML/JavaScript application
- Provider modules in `backend/models/` handle specific provider API calls
- API key rotation is handled by the KeyRotator class in `utils.py`