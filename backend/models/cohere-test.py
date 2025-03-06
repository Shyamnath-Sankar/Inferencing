import cohere

co = cohere.ClientV2(api_key='NYEQhh6CwVF3dCo57n25032m4s0FurCYI73IYWb5')

response = co.chat_stream(
    model="command-r-plus-08-2024",
    messages=[{"role": "user", "content": "write a story about a drogon"}],
)

for event in response:
    if event.type == "content-delta":
        print(event.delta.message.content.text, end="")
