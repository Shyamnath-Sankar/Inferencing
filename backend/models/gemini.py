import google.generativeai as genai
import asyncio
from typing import AsyncGenerator

async def run_model_stream(api_key: str, model: str, prompt: str):
    """
    Run the Gemini model with streaming response.
    
    Args:
        api_key: The API key to use for this request
        model: The model name to use
        prompt: The user's input prompt
        
    Yields:
        str: Chunks of the generated response
    """
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model with name from MODELS.csv
        model_instance = genai.GenerativeModel(model)
        
        # Start the streaming response using async executor
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: model_instance.generate_content(
                prompt,
                stream=True
            )
        )
        
        # Process chunks with async handling
        for chunk in response:
            if chunk.text:
                # Use asyncio.sleep to prevent blocking
                await asyncio.sleep(0)
                yield chunk.text
        
    except Exception as e:
        raise Exception(f"Error with Gemini API: {str(e)}")

async def run_model(api_key: str, model: str, prompt: str) -> str:
    """
    Run the Gemini model with the provided API key and prompt (non-streaming).
    
    Args:
        api_key: The API key to use for this request
        model: The model name to use
        prompt: The user's input prompt
        
    Returns:
        str: The generated response
    """
    response = ""
    async for chunk in run_model_stream(api_key, model, prompt):
        response += chunk
    return response
