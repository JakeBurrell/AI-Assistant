import os
import sys
from dotenv import load_dotenv
from google import genai
from system_prompt import system_prompt
from google.genai import types
from functions.call_functions import call_function, available_functions


def main():
    load_dotenv()
    verbose = False

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]

    if not args :
        print("AI Code Assistant")
        print('\nUsage: Python main.py "your prompt here"')
        print('Example: Python main.py "How to build a calculator app"')
        sys.exit(1)
    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    
    client = genai.Client(api_key=api_key)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents = messages,
        config = types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part)
            if function_call_result.parts[0].function_response.response:
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                raise Exception("Invalid response from call function")
    else:
        print(response.text)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == main():
    main()
