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