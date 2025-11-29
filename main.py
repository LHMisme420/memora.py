from agents.phi3_memory_reasoner import reasoner

# Inside your main loop, add this:
        if query.startswith("why ") or query.startswith("when ") or query.startswith("how did i feel"):
            console.print("[bold cyan]Asking my second brain...[/bold cyan]")
            answer = reasoner.ask(query)
            console.print(f"[bold white]{answer}[/bold white]\n")
