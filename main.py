import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    print("Hello from python-ai-agent!")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set, found, or is empty.")
    client = genai.Client(api_key = api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type = str, help = "User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    
   

    
    response = client.models.generate_content(model = "gemini-2.5-flash", contents = messages)
    # Defensive check
    if response.usage_metadata is None:
        raise RuntimeError("Gemini API returned no usage metadata. This may indicate a failed or incomplete API response."
                           )
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    
    print(response.text)

if __name__ == "__main__":
    main()
