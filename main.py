import os
import sys
import logging
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

from config import GROQ_API_KEY, LOG_LEVEL, MEMORY_DIR
from agents import PlannerAgent, ExecutorAgent
from memory import ShortTermMemory, LongTermMemory
from tools.notes import NOTES_DIR

# Setup logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()

def main():
    if not GROQ_API_KEY:
        console.print("[red]Error: GROQ_API_KEY is missing from environment. Please define it in your .env file.[/red]")
        sys.exit(1)

    console.print(Panel.fit("[bold blue]AI Personal Task & Decision Assistant[/bold blue]\n[green]Ready to help you plan, research, and execute tasks![/green]"))

    # Initialize components
    short_term_memory = ShortTermMemory()
    long_term_memory_path = os.path.join(MEMORY_DIR, "long_term.json")
    long_term_memory = LongTermMemory(filepath=long_term_memory_path)
    
    planner = PlannerAgent(api_key=GROQ_API_KEY)
    executor = ExecutorAgent(api_key=GROQ_API_KEY)

    # Main interaction loop
    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            if user_input.lower() in ['exit', 'quit', 'q']:
                break
                
            short_term_memory.add_message("user", user_input)
            
            # Extract basic context
            context_str = short_term_memory.get_context_string()
            
            # Fetch relevant long term memory
            relevant_ltm = long_term_memory.retrieve_relevant(user_input, top_k=3)
            ltm_context = "\n".join(relevant_ltm) if relevant_ltm else "No relevant long-term memories found."
            
            # 1. Plan
            console.print("[yellow]Planning steps...[/yellow]")
            plan = planner.plan(user_input, short_term_context=context_str, long_term_context=ltm_context)
            
            for step in plan:
                console.print(f"[dim]Step {step.get('step_number')}: {step.get('tool')} ({step.get('reasoning')})[/dim]")
                
            # 2. Execute
            console.print("[yellow]Executing plan...[/yellow]")
            final_answer = executor.execute_plan(plan, user_input)
            
            # 3. Handle Auto-Memory storage for generic ideas organically,
            # Though our notebook tool explicitly saves if required. Let's just track short term context.
            short_term_memory.add_message("assistant", final_answer)
            
            console.print(Panel(Markdown(final_answer), title="[bold green]Assistant[/bold green]", border_style="green"))
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"\n[red]Unhandled Error: {str(e)}[/red]")
            
    console.print("[blue]Goodbye![/blue]")

if __name__ == "__main__":
    main()
