import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function
import json
import sys
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")


def gen_response(messages):
    if api_key == None:
            raise RuntimeError("none api key")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        )

    return client.chat.completions.create(
            model="openrouter/free",
            messages = messages,
            tools = available_functions
        )



def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for i in range(20):
        response =  gen_response(messages)
        if response.choices[0].message.content:
            message = response.choices[0].message.content
            msg = {"role":"assistant", "content":message}
            messages.append(msg)
        if response.choices[0].message.tool_calls:
             for tool_call in response.choices[0].message.tool_calls:
                tool_call_id = tool_call.id
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
                result_message = call_function(tool_call)
                res = {"role":"tool", "tool_call_id":tool_call_id, "content":result_message['content']}
                if not result_message["content"]:
                    raise Exception("Empty result")
                if args.verbose:
                        print(f"-> {result_message['content']}")
                messages.append(res)

        elif not response.choices[0].message.tool_calls:
            message = response.choices[0].message.content
            msg = {"role":"assistant", "content":message}
            messages.append(msg)
            print(messages)
            break
        elif i == 19:
            print("Attempts reached limits, did not finish the task")
            sys.exit(1)



    # for tool_call in response.choices[0].message.tool_calls:

    #     function_args = json.loads(tool_call.function.arguments or "{}")
    #     print(f"Calling function: {tool_call.function.name}({function_args})")

    #     result_message = call_function(tool_call, args.verbose)
    #     if not result_message["content"]:
    #          raise Exception("Empty result")
    #     if args.verbose:
    #          print(f"-> {result_message['content']}")

    # if response.usage == None:
    #     raise RuntimeError("No response")


    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)


main()