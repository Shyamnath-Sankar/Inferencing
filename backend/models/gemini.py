from openai import OpenAI

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
        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
        
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
