import requests

def run_model(api_key: str, model: str, prompt: str) -> str:
    """
    Run the SambaNova model with the provided API key and prompt.
    
    Args:
        api_key: The API key to use for this request
        model: The model name to use
        prompt: The user's input prompt
        
    Returns:
        str: The generated response
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
            "Qwen 2.5 Coder 32B": "Qwen2.5-Coder-32B-Instruct"  # Updated to exact model name
        }
        
        samba_model = model_map.get(model, model)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": samba_model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "top_p": 0.95
        }
        
        response = requests.post(
            "https://api.sambanova.ai/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Error code: {response.status_code} - {response.json()}")
            
        return response.json()["choices"][0]["message"]["content"]
        
    except Exception as e:
        raise Exception(f"Error with SambaNova API: {str(e)}")