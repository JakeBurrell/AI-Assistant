import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    verbose = False

    args = sys.argv[1:]

    if not args :
        print("AI Code Assistant")
        print('\nUsage: Python main.py "your prompt here"')
        print('Example: Python main.py "How to build a calculator app"')
        sys.exit(1)

    if len(args) > 1 and args[1] == "--verbose":
        verbose = True

    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    
    client = genai.Client(api_key=api_key)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents = messages
    )
    if verbose:
        print("User prompt:")

    print(response.text)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == main():
    main()
