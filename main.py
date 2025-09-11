import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time
from google.genai import errors as genai_errors

from functions.call_function import call_function, available_functions
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.
You can perform the following function:

- List files and directories (get_files_info)
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
All paths must be relative to the working directory. Do not specify the working directory yourself.
"""

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    run_agent(
        client=client,
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        available_functions=available_functions,  # see note below
        verbose=verbose,
    )


def gen_with_retry(client, *, model, contents, config, max_retries=5, base_delay=0.5):
    attempt = 0
    while True:
        try:
            return client.models.generate_content(model=model, contents=contents, config=config)
        except genai_errors.ServerError as e:
            code = getattr(e, "status_code", None)
            if code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                time.sleep(base_delay * (2 ** attempt))
                attempt += 1
                continue
            raise

def run_agent(client, user_prompt, system_prompt,available_functions, verbose=False):
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    config = types.GenerateContentConfig(
        tools=available_functions,
        system_instruction=system_prompt,
    )
    for _ in range(10):
        resp = gen_with_retry(
            client,
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config
        )
        model_msg = resp.candidates[0].content
        messages.append(model_msg)
        fn_call = next(
            (p.function_call for p in model_msg.parts if getattr(p, "function_call", None)),
            None
        )
        if not fn_call:
            final_text = (resp.text or "").strip()
            print(final_text if final_text else "No output produced.")
            break
        tool_msg = call_function(fn_call, verbose=verbose)
     
        if verbose:
            print(tool_msg.parts[0].function_response.response["result"])

     
        messages.append(tool_msg)
 
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
    main()
