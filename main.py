import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv



def main():
    if len(sys.argv) <2:
        print("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)
    user_prompt = sys.argv[1]   
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose = "--verbose" in sys.argv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)])
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )
    print(response.text)
    print('Prompt tokens:', response.usage_metadata.prompt_token_count)
    print('Response tokens:', response.usage_metadata.candidates_token_count)

    if verbose:
        print("User prompt:", user_prompt)
        print('Prompt tokens:', response.usage_metadata.prompt_token_count)
        print('Response tokens:', response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
