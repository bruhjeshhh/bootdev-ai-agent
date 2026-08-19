import os
import argparse
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENAPI_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ],
)

print("Prompt tokens: ", response.usage.prompt_tokens)
print("Response tokens: ", response.usage.completion_tokens - response.usage.prompt_tokens)
print("Response: " + response.choices[0].message.content)