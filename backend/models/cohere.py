import cohere
import asyncio
from typing import AsyncGenerator

async def run_model_stream(api_key: str, model: str, prompt: str):
    """
    Run the Cohere model with streaming response.
    
    Args:
        api_key: The API key to use for this request
        model: The model name to use
        prompt: The user's input prompt
        
    Yields:
        str: Chunks of the generated response
    """
    try:
        client = cohere.Client(api_key=api_key)
        
        # Create chat message with streaming
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat(
                chat_history=[],
                message=prompt,
                model=model,  # Use model name directly from MODELS.csv
                stream=True,
                temperature=0.7
            )
        )
        
        # Process each chunk
        for event in response:
            if hasattr(event, 'text') and event.text:
                # Use asyncio.sleep to prevent blocking
                await asyncio.sleep(0)
                yield event.text
        
    except Exception as e:
        raise Exception(f"Error with Cohere API: {str(e)}")

async def run_model(api_key: str, model: str, prompt: str) -> str:
    """
    Run the Cohere model with the provided API key and prompt (non-streaming).
    
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