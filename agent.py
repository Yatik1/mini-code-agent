import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from prompts import system_prompt
from tools import available_tools
from rich.console import Console

console = Console()
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def ask_llm(messages):
    response = client.chat.completions.create(
        model="gemini-2.0-flash", 
        response_format={"type": "json_object"},
        messages=messages
    )
    return json.loads(response.choices[0].message.content)

def process_action(parsed_output):
    tool_name = parsed_output.get("function")
    tool_input = parsed_output.get("input")

    try:
        if tool_name in available_tools:
            tool_fn = available_tools[tool_name]["fn"]
            if isinstance(tool_input, str):
                tool_input = json.loads(tool_input)
            output = tool_fn(tool_input)
            return {"step": "observe", "output": output}
        else:
            return {"step": "observe", "output": f"Tool '{tool_name}' not found."}
    except Exception as e:
        return {"step": "observe", "output": f"Error: {str(e)}"}