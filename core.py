from agent import client, ask_llm, process_action
from prompts import system_prompt
from rich.console import Console

messages = [{"role": "system", "content": system_prompt}]
console = Console()

def main():
    while True:
        user_input = input("\n🗣️  Your command:\n> ")
        messages.append({"role": "user", "content": user_input})

        while True:
            parsed_output = ask_llm(messages)
            messages.append({"role": "assistant", "content": str(parsed_output)})

            step = parsed_output.get("step")

            if step in ["start", "plan"]:
                console.print(f"[bold blue]🧠 {parsed_output['content']}[/bold blue]")
                continue

            elif step == "action":
                observation = process_action(parsed_output)
                console.print(f"[yellow]⚙️  Executing {parsed_output['function']}[/yellow]")
                messages.append({"role": "assistant", "content": str(observation)})
                continue

            elif step == "observe":
                console.print(f"[green]🔍 {parsed_output.get('output')}[/green]")
                continue

            elif step == "output":
                console.print(f"[bold green]✅ {parsed_output['content']}[/bold green]")
                break

if __name__ == "__main__":
    main()
