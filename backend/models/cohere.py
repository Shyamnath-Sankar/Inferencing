import cohere

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
        # Map friendly model names to Cohere's actual model names
        model_map = {
            "Command R": "command",
            "Command R7B": "command-r",
            "Command R+": "command-light"
        }
        
        cohere_model = model_map.get(model, model)
        client = cohere.ClientV2(api_key=api_key)
        
        response = client.chat_stream(
            model=cohere_model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        for event in response:
            if event.type == "content-delta":
                yield event.delta.message.content.text
        
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