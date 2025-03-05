# Openai based gemini inference with streaming response 
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCHJOkMGNtx5TUbKNCOHSSttOWJm9qbwH0",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
  model="gemini-2.0-flash",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a story about a dragon."}
  ],
  stream=True
)

for chunk in response:
    print(chunk.choices[0].delta)



# Openai based gemini inference
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCHJOkMGNtx5TUbKNCOHSSttOWJm9qbwH0",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)

print(response.choices[0].message)




