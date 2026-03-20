import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0,
                tools=[available_functions],
            ),
        )

        # Preserve the model's output in conversation history.
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # If the model asked to call functions, execute them and send results back.
        if response.function_calls:
            function_results = []

            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)

                if not function_call_result.parts:
                    raise Exception("Function call returned no parts")

                function_response = function_call_result.parts[0].function_response
                if function_response is None:
                    raise Exception("Missing function response")

                if function_response.response is None:
                    raise Exception("Function response is empty")

                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_response.response}")

            if function_results:
                # IMPORTANT: tool, not user
                messages.append(types.Content(role="tool", parts=function_results))

        else:
            # Final natural-language answer from the model
            print(response.text)
            sys.exit(0)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            if response.usage_metadata:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Agent reached maximum iterations without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()