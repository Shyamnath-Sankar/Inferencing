import os
import openai

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"
)       
completion = client.chat.completions.create(
    model="qwen-2.5-coder-32b",
    messages=[
        {
            "role": "user",
            "content": "hi\n"
        },
        {
            "role": "user",
            "content": "hi\n"
        },
        {
            "role": "assistant",
            "content": "<think>\nOkay, the user just said \"hi.\" I should respond in a friendly and welcoming way.\n\nI want to make sure they feel comfortable asking for help.\n\nMaybe I'll ask how I can assist them today.\n\nKeeping it open-ended encourages them to share what they need.\n</think>\n\nHello! How can I assist you today?"
        }
    ],
    temperature=0.6,
    max_completion_tokens=4096,
    top_p=0.95,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
