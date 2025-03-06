import os
import openai

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"
)       
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)