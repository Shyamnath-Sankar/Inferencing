import requests
import sseclient
import json

def test_inference():
    # Base URL of the API
    base_url = "http://localhost:8000"
    
    try:
        # First, get available models
        models_response = requests.get(f"{base_url}/models")
        models = models_response.json()
        print("Available models:")
        for model in models:
            print(f"- {model['model']} ({model['provider']})")
        print("\n")
        
        # Example prompt
        prompt = "Tell me a short story about a robot"
        model = "Llama-3.1-Tulu-3-405B"  # You can change this to any available model
        
        print(f"Using model: {model}")
        print(f"Prompt: {prompt}")
        print("\nResponse:")
        
        # Create SSE client for streaming response
        url = f"{base_url}/generate?model={requests.utils.quote(model)}&prompt={requests.utils.quote(prompt)}"
        response = requests.get(url, stream=True)
        client = sseclient.SSEClient(response)
        
        # Process the streamed response
        for event in client.events():
            if event.data == "[DONE]":
                break
                
            try:
                data = json.loads(event.data)
                if "error" in data:
                    print(f"Error: {data['error']}")
                    break
                elif "content" in data:
                    # Print content without newline to show streaming effect
                    print(data["content"], end="", flush=True)
            except json.JSONDecodeError:
                continue
                
        print("\n\nGeneration complete!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Make sure to install required packages:
    # pip install requests sseclient-py
    test_inference()
