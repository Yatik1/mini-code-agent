from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_command(command):
    result = os.system(command=command)
    return result 

available_tools = {
    "run_command": {
        "fn" : run_command,
        "description":"Takes a command as input and execute it on system and returns output"
    }
}

system_prompt = f"""
You are an helpfull AI Code file management system and an expert code assistant who is specilaized in resolving user query.
For the given appropriate query you deligently try to resolve the query by working on start,plan,action and observer mode.

For the given user query and available tools, plan the step by step by execution. Based on the planning, select the relevant tool from the available tool.
And based on the tool selected you perform an action to call the tool.
Then wait for the observation and based on the observation from the tool called resolve the user query.

Rules:
1. Follow the Ouput JSON format
2. Always perform one step at a time and wait for the next input
3. Carefully analyse the user query

Output JSON format:
{{
    "step":"string",
    "content":"string",
    "function":"The name of the function if the step is action",
    "input":"The input parameter for the function"
}}

Available Tools:
- run_command : Takes a command as an input and execute it on the system and return output

Example:
User Query: Create an file called sum.py and write a code of it in the file
Output:{{"step":"start", "content":"The user wants a function which can do addition of two numbers"}}
Output:{{"step":"action","function":"run_command", "input":"touch sum.py"}}
Output:{{"step":"plan","content":"Understanding the concept and solving user query"}}
Output:{{"step":"plan","content":"Opening the file to add the content into it"}}
Output:{{"step":"observe","output":"The code has been written in the created file"}}
Output:{{"step":"output","content":"File is ready. Is there anything you want me to change?"}}
"""

messages = [
    {"role":"system", "content":system_prompt}
]

while True:
    user_query = input(">")
    messages.append({"role":"user","content":user_query})
    
    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type":"json_object"},
            messages=messages
        )
    
        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({"role":"assistant","content":json.dumps(parsed_output)})
    
        if parsed_output.get("step") == "start" or parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get("content")}")
            continue
        
        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")
    
            if tool_name in available_tools:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})
                continue
            
        if parsed_output.get("step") == "output":
            break



