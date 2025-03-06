from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import logging
import logging.config

from core.config import API_HOST, API_PORT, CORS_SETTINGS, LOG_CONFIG
from core.exceptions import APIError, handle_api_error
from core.text_generation import text_generator

# Configure logging
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Text Generation API",
             description="API for text generation using multiple AI providers",
             version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    **CORS_SETTINGS
)

class PromptRequest(BaseModel):
    model: str
    prompt: str

@app.get("/models")
async def get_models():
    """Get list of all available models."""
    try:
        return text_generator.get_available_models()
    except APIError as e:
        error_response = handle_api_error(e)
        raise HTTPException(
            status_code=error_response["status_code"],
            detail=error_response["detail"]
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_models: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def generate_stream(model: str, prompt: str):
    """Stream generator for text generation."""
    try:
        async for chunk in text_generator.generate_stream(model, prompt):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
    except APIError as e:
        error_response = handle_api_error(e)
        yield f"data: {json.dumps({'error': error_response['detail']})}\n\n"
    except Exception as e:
        logger.error(f"Unexpected error in generate_stream: {str(e)}")
        yield f"data: {json.dumps({'error': 'Internal server error'})}\n\n"
    finally:
        yield "data: [DONE]\n\n"

@app.post("/generate")
async def generate_response(request: PromptRequest):
    """Generate response using selected model."""
    try:
        logger.info(f"Received request for model: {request.model}")
        return StreamingResponse(
            generate_stream(request.model, request.prompt),
            media_type="text/event-stream"
        )
    except APIError as e:
        error_response = handle_api_error(e)
        raise HTTPException(
            status_code=error_response["status_code"],
            detail=error_response["detail"]
        )
    except Exception as e:
        logger.error(f"Unexpected error in generate_response: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)