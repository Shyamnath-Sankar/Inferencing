import openai

def run_model(api_key: str, model: str, prompt: str) -> str:
    """
    Run the Groq model with the provided API key and prompt.
    
    Args:
        api_key: The API key to use for this request
        model: The model name to use (from GROQ MODELS column in MODELS.csv)
        prompt: The user's input prompt
        
    Returns:
        str: The generated response
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
        
        completion = client.chat.completions.create(
            model=groq_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            max_tokens=4096,  # Changed from max_completion_tokens
            top_p=0.95,
            stream=True,
            stop=None
        )

        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        
        return response
        
    except Exception as e:
        raise Exception(f"Error with Groq API: {str(e)}")
