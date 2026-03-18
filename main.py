import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Create parser
    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]



    for _ in range(20):
    
        function_results = []
        # call the model, handle responses, etc.

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config = types.GenerateContentConfig(system_instruction = system_prompt, 
            temperature = 0,
            tools = [available_functions],
            )
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
                
        
        
        # Create an empty list to store results from any function calls the LLM makes.
        # These results will be sent back to the model later.

        if response.function_calls:
            # Check if the LLM requested any function calls.
            # This will be a list of FunctionCall objects (could be multiple).

            for function_call in response.function_calls:
                # Loop through each function the LLM wants to invoke.

                function_call_result = call_function(function_call, args.verbose)
                # Execute the requested function and return the result
                # wrapped in a Content object.

                if not function_call_result.parts:
                    raise Exception("Function call returned no parts")
                # Ensure the result contains at least one Part.
                # If empty, something went wrong internally.

                function_response = function_call_result.parts[0].function_response
                # Extract the FunctionResponse from the first Part.

                if function_response is None:
                    raise Exception("Missing function response")
                # Verify the FunctionResponse exists (defensive check).

                if function_response.response is None:
                    raise Exception("Function response is empty")
                # Ensure the actual response payload (dict) exists.

                function_results.append(function_call_result.parts[0])
                # Store the Part (not the full Content object) for later use.

                if args.verbose:
                    print(f"-> {function_response.response}")
                # If verbose mode is enabled, print the raw function output
                # (usually a dictionary like {"result": "..."} or {"error": "..."}).

            if function_results:
                messages.append(types.Content(role="user", parts=function_results))

        else:
            # If no function calls were made by the LLM:

            print(response.text)
            # Simply print the model's text response.
            break

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")

            prompt_tokens = response.usage_metadata.prompt_token_count
            candidate_tokens = response.usage_metadata.candidates_token_count

            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {candidate_tokens}")

    
    print("Agent reached maximum iterations without a final response")
    sys.exit(1)






if __name__ == "__main__":
    main()
