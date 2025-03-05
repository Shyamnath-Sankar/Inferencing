import os
import openai

client = openai.OpenAI(
    api_key="2b1f2b2b-4867-4991-8a30-f43c11469cdf",
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model="Qwen2.5-Coder-32B-Instruct",
    messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"Write a poem about jai samyukth who fell in love"}],
    temperature=0.1,
    top_p=0.1
)

print(response.choices[0].message.content)