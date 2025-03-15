import httpx
import json
from typing import AsyncGenerator

async def run_model_stream(api_key: str, model: str, prompt: str):
    """
    Run the SambaNova model with streaming response.
    
    Args:
        api_key: The API key to use for this request
        model: The model name to use
        prompt: The user's input prompt
        
    Yields:
        str: Chunks of the generated response
    """
    try:
        # Configure HTTP client with appropriate headers and SSL settings
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        async with httpx.AsyncClient(
            base_url="https://api.sambanova.ai/v1",
            headers=headers,
            verify=True,
            timeout=httpx.Timeout(60.0, read=300.0)
        ) as client:
            # Make streaming request
            async with client.stream(
                "POST",
                "/chat/completions",
                json={
                    "model": model,  # Use model name directly from MODELS.csv
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": True,
                    "temperature": 0.7,
                    "max_tokens": 2048
                }
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.startswith("data: "):
                        data = line[6:].strip()
                        if data == "[DONE]":
                            break
                            
                        try:
                            chunk_data = json.loads(data)
                            if chunk_data.get("choices") and chunk_data["choices"][0].get("delta"):
                                content = chunk_data["choices"][0]["delta"].get("content")
                                if content:
                                    yield content
                        except Exception as e:
                            print(f"Error parsing chunk: {e}")
                            continue
                            
    except httpx.HTTPError as e:
        raise Exception(f"HTTP error with SambaNova API: {str(e)}")
    except Exception as e:
        raise Exception(f"Error with SambaNova API: {str(e)}")

async def run_model(api_key: str, model: str, prompt: str) -> str:
    """
    Run the SambaNova model with the provided API key and prompt (non-streaming).
    
    Args:
        api_key: The API key to use for this request
        model: The model name to use
        prompt: The user's input prompt
        
    Returns:
        str: The generated response
    """
    response_text = ""
    async for chunk in run_model_stream(api_key, model, prompt):
        response_text += chunk
    return response_text