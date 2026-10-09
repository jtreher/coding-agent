import os
import argparse
from call_function import call_function, available_functions
import json

from prompts import prompts
from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    _ = load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == "None":
        raise RuntimeError("Please configure a missing openrouter api key in your .env or environment")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {
            "role" : "system",
            "content": prompts.system_prompt
        },
        {
            "role" : "user",
            "content" : args.user_prompt
        }
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0
        )

        if response.usage == None:
            raise RuntimeError("Failed to contact API for chat completion")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message

        # Append to our chat context window
        messages.append(message)

        if message.tool_calls == None or len(message.tool_calls) == 0:
            print(message.content)
            return

        for tool_call in message.tool_calls:
            result = call_function(tool_call, args.verbose)
            if args.verbose:
                print(f"-> {result['content']}")
            messages.append(result)

    # We existed the loop naturally, which means we never got a result.
    exit(1)


if __name__ == "__main__":
    main()
