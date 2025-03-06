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
        client = openai.OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
        
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model,
            stream=True
        )

        for chunk in completion:
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
    try:
        client = openai.OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"Error with Groq API: {str(e)}")
