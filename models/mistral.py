import os
from mistralai import Mistral

api_key = "gZkpXZUIvz1ryxpyODGmsommNbryox2s"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

stream_response = client.chat.stream(
    model = model,
    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
)

for chunk in stream_response:
    print(chunk.data.choices[0].delta.content)