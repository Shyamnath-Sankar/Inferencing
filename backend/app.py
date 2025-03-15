from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import logging
import logging.config
import os

from core.config import API_HOST, API_PORT, CORS_SETTINGS, LOG_CONFIG
from core.exceptions import APIError, handle_api_error
from core.text_generation import text_generator

# Configure logging
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Text Generation API",
             description="API for text generation using multiple AI providers",
             version="1.0.0")

# Enable CORS with specific headers for SSE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Cache-Control"]
)

# Mount static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

class PromptRequest(BaseModel):
    model: str
    prompt: str

@app.get("/")
async def read_root():
    """Serve the frontend HTML."""
    return FileResponse(os.path.join(frontend_dir, 'index.html'))

@app.get("/models")
async def get_models():
    """Get list of all available models."""
    try:
        # Return models as a JSON array
        return JSONResponse(content=text_generator.get_available_models())
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
            # Add extra newline to ensure proper event separation
            yield f"data: {json.dumps({'content': chunk})}\n\n"
    except APIError as e:
        error_response = handle_api_error(e)
        yield f"data: {json.dumps({'error': error_response['detail']})}\n\n"
    except Exception as e:
        logger.error(f"Unexpected error in generate_stream: {str(e)}")
        yield f"data: {json.dumps({'error': 'Internal server error'})}\n\n"
    finally:
        yield "data: [DONE]\n\n"

@app.get("/generate")
@app.post("/generate")
async def generate_response(request: Request):
    """Generate response using selected model (supports both GET and POST)."""
    try:
        # Handle both GET and POST methods
        if request.method == "GET":
            params = dict(request.query_params)
            model = params.get("model")
            prompt = params.get("prompt")
        else:
            body = await request.json()
            model = body.get("model")
            prompt = body.get("prompt")

        if not model or not prompt:
            raise HTTPException(status_code=400, detail="Missing model or prompt parameter")

        logger.info(f"Received {request.method} request for model: {model}")
        
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable buffering for nginx
        }
        
        return StreamingResponse(
            generate_stream(model, prompt),
            media_type="text/event-stream",
            headers=headers
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