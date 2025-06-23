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
    for i in range(20):
        is_funct = generate_content(client, messages, verbose)
        if not is_funct:
            break


def generate_content(client, messages, verbose):
    is_funct = False

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents = messages,
        config = types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )

    if isinstance(response.candidates, list):
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part)
            if function_call_result.parts[0].function_response.response:
                messages.append(function_call_result)
                print(f"\t - Calling function: {function_call_part.name}")
                is_funct = True
                #print(f"-> {function_call_result.parts[0].function_response.response}")
                #print(response.text)
            else:
                raise Exception("Invalid response from call function")
    else:
        print(response.text)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    return is_funct


if __name__ == main():
    main()
