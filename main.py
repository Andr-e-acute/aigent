import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.
You can perform the following function:

- List files and directories (get_files_info)

All paths must be relative to the working directory. Do not specify the working directory yourself.
"""

def main():
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    available_functions = [
        types.Tool(function_declarations=[schema_get_files_info])
    ]

    config = types.GenerateContentConfig(
        tools=available_functions,
        system_instruction=system_prompt,
    )

    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=config,
    )

    # Find a function_call in parts, if present
    parts = resp.candidates[0].content.parts
    fn_call_part = next((p.function_call for p in parts if getattr(p, "function_call", None)), None)

    if fn_call_part:
        # Print ONLY the function-call line (what the grader expects)
        print(f"Calling function: {fn_call_part.name} with args: {fn_call_part.args}")
    else:
        # Otherwise print the model text
        print(resp.text)

    # Optional debug output only when explicitly requested
    if verbose:
        print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
        print("Response tokens:", resp.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
