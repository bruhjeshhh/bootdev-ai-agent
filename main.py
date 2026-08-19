import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENAPI_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ],
)

print(response.choices[0].message.content)