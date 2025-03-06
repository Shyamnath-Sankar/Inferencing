import openai

async def run_model_stream(api_key: str, model: str, prompt: str):
    """
    Run the Groq model with streaming response.
    
    Args:
        api_key: The API key to use for this request
        model: The model name to use
        prompt: The user's input prompt
        
    Yields:
        str: Chunks of the generated response
    """
    try:
        # Map friendly model names to Groq's actual model names
        model_map = {
            "deepseek-r1-distill-llama-70b": "mixtral-8x7b-32768",
            "llama-3.3-70b-versatile": "llama3-70b-8192",
            "llama-3.3-70b-specdec": "llama3-8b-8192",
            "llama-3.2-1b-preview": "llama-guard-3-8b",
            "llama-3.2-3b-preview": "gemma2-9b-it",
            "llama-3.1-8b-instant": "llama-3.2-11b-vision-preview",
            "llama3-70b-8192": "llama3-70b-8192",
            "llama3-8b-8192": "llama3-8b-8192",
            "llama-guard-3-8b": "llama-guard-3-8b",
            "mixtral-8x7b-32768": "mixtral-8x7b-32768",
            "gemma2-9b-it": "gemma2-9b-it",
            "llama-3.2-11b-vision-preview": "llama-3.2-11b-vision-preview",
            "llama-3.2-90b-vision-preview": "llama-3.2-90b-vision-preview"
        }

        groq_model = model_map.get(model, model)
        client = openai.OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
        
        response = client.chat.completions.create(
            model=groq_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            max_tokens=4096,
            top_p=0.95,
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
        
    except Exception as e:
        raise Exception(f"Error with Groq API: {str(e)}")

async def run_model(api_key: str, model: str, prompt: str) -> str:
    """
    Run the Groq model with the provided API key and prompt (non-streaming).
    
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
