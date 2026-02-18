import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import call_function
from functions.call_function import available_functions

def main():
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set, found, or is empty.")
    client = genai.Client(api_key = api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type = str, help = "User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    
    for _ in range(20):

        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config = types.GenerateContentConfig(
                tools = [available_functions], system_instruction=system_prompt),
            )
        # Defensive check
        if response.usage_metadata is None:
            raise RuntimeError("Gemini API returned no usage metadata. This may indicate a failed or incomplete API response."
                            )
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        if args.verbose:
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        if not response.candidates:
            raise RuntimeError("Gemini API returned no candidates.")
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)
        if response.function_calls:
            function_response = []
            for call in response.function_calls:
                function_result = call_function(call, verbose=args.verbose)

                if not function_result.parts:
                    raise Exception("The function result should have parts!")
                
                tool_response_part = function_result.parts[0]
                function_response.append(tool_response_part)

        if response.function_calls:
            messages.append(types.Content(role="user", parts=function_response))
            continue
        print(f"Final response:\n{response.text}")
        return 
    print("Conversation ended.")
    sys.exit(1)

    
    
    
    
        
    

if __name__ == "__main__":
    main()
