import os
import json
import argparse
from dotenv import load_dotenv

from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("OPENAPI_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    message = response.choices[0].message

    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            if not result_message["content"]:
                raise Exception("Function returned empty content")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print("Response:", message.content)


if __name__ == "__main__":
    main()