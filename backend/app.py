from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import importlib
from utils import key_rotator
import logging
import json
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    model: str
    prompt: str

class ModelInfo(BaseModel):
    model: str
    provider: str

@app.get("/models", response_model=List[ModelInfo])
async def get_models():
    """Get list of all available models."""
    try:
        return key_rotator.get_available_models()
    except Exception as e:
        logger.error(f"Error in get_models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_stream(provider_module, api_key: str, model: str, prompt: str):
    """Generate streaming response."""
    try:
        async for chunk in provider_module.run_model_stream(api_key, model, prompt):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in generate_stream: {error_msg}")
        yield f"data: {json.dumps({'error': error_msg})}\n\n"
    finally:
        yield "data: [DONE]\n\n"

@app.post("/generate")
async def generate_response(request: PromptRequest):
    """Generate response using selected model and rotating API key."""
    try:
        logger.info(f"Received request for model: {request.model}")
        
        # Get provider for the selected model
        provider = key_rotator.get_provider_for_model(request.model)
        logger.info(f"Provider determined: {provider}")
        
        # Get next API key for the provider
        try:
            api_key = key_rotator.get_next_key(provider)
            logger.info(f"Got API key for provider: {provider}")
        except ValueError as e:
            logger.error(f"API key error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        
        # Import the appropriate provider module
        try:
            module_name = provider.lower().split()[0]  # Get first word in lowercase
            logger.info(f"Attempting to import module: models.{module_name}")
            provider_module = importlib.import_module(f"models.{module_name}")
        except ImportError as e:
            logger.error(f"Module import error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Provider module not found for: {provider}"
            )
        
        # Return streaming response
        return StreamingResponse(
            generate_stream(provider_module, api_key, request.model, request.prompt),
            media_type="text/event-stream"
        )
            
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"General error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)