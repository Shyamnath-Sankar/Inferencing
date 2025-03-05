# AI Model Inference System

This application provides a web interface to interact with various AI models from different providers (GROQ, COHERE, SambaNova, and GEMINI) with automatic API key rotation.

## Project Structure

```
.
├── frontend/
│   ├── index.html
│   └── script.js
├── backend/
│   ├── app.py
│   └── requirements.txt
├── models/
│   ├── groq.py
│   ├── cohere-test.py
│   ├── sambanova.py
│   └── gemini.py
├── MODELS.csv
└── apikeys.csv
```

## Setup Instructions

1. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start the backend server:
```bash
python app.py
```

3. Open the frontend:
- Simply open `frontend/index.html` in your web browser
- Or use a local server to serve the frontend files

## Features

- Clean and intuitive user interface
- Models grouped by provider
- Automatic API key rotation for load balancing
- Real-time response display
- Error handling and user feedback

## How it Works

1. Select any available model from the dropdown menu
2. Enter your prompt in the text area
3. Click "Generate Response" to get the AI's response
4. The system will automatically:
   - Determine the appropriate provider for the selected model
   - Select the next available API key in rotation for that provider
   - Route the request to the correct model implementation
   - Display the response with provider information

## Note

Make sure both MODELS.csv and apikeys.csv files are present in the root directory as they contain the model mappings and API keys for the different providers.# Inferencing-Model
# Inferencing
