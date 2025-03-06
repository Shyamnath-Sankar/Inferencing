import openai

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
        # Map friendly model names to SambaNova's actual model names
        model_map = {
            "Llama 3.1 8B": "llama-3-1-8b",
            "Llama 3.1 70B": "llama-3-1-70b",
            "Llama 3.1 405B": "llama-3-1-405b",
            "Llama 3.2 1B": "llama-3-2-1b",
            "Llama 3.2 3B": "llama-3-2-3b",
            "Llama 3.2 11B": "llama-3-2-11b",
            "Llama 3.2 90B": "llama-3-2-90b",
            "Llama 3.3 70B": "llama-3-3-70b",
            "Llama Guard 3 8B": "llama-guard-3-8b",
            "Qwen 2.5 72B": "qwen-2-5-72b",
            "Qwen 2.5 Coder 32B": "Qwen2.5-Coder-32B-Instruct"
        }
        
        samba_model = model_map.get(model, model)
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.sambanova.ai/v1"
        )
        
        response = client.chat.completions.create(
            model=samba_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            top_p=0.95,
            stream=True  # Enable streaming
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
        
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
    response = ""
    async for chunk in run_model_stream(api_key, model, prompt):
        response += chunk
    return response