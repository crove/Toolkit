import typer
from rich.table import Table
from rich.console import Console
from cli_taskmanager.controller.task_service import TaskService

app = typer.Typer()
console = Console()

def get_service():
    return TaskService()

@app.command()
def add(task: str):
    service = get_service()
    new_task = service.add_task(task)
    console.print(f"[green]Added:[/green] {new_task.description} (ID: {new_task.id})")

@app.command(name="done")
def mark_done(task_id: int):
    service = get_service()
    updated = service.mark_done(task_id)
    if updated:
        console.print(f"[cyan]Done:[/cyan] {updated.description} (ID: {updated.id})")
    else:
        console.print(f"[red]Task with ID {task_id} not found[/red]")

@app.command(name="del")
def delete(task_id: int):
    service = get_service()
    success = service.delete_task(task_id)
    if success:
        console.print(f"[red]Deleted task with ID {task_id}")
    else:
        console.print(f"[red]Task with ID {task_id} not found[/red]")

@app.command(name="clear")
def clear_done():
    service = get_service()
    cleared = service.clear_done()
    if cleared:
        console.print(f"[green]Cleared {cleared} completed tasks[/green]")
    else:
        console.print("[yellow]No done tasks to clear.[/yellow]")

@app.command(name="ls")
def list(
    status: str = typer.Option(
        "all",
        "--status",
        "-s",
        help="Filter tasks by status: all | done | todo",
        show_default=True,
    ),
):
    service = get_service()
    tasks = service.list_tasks(status)
    table = Table(title=f"Tasks ({status})")
    table.add_column("ID", style="bold")
    table.add_column("Status")
    table.add_column("Task")
    for t in tasks:
        icon = "✓" if t.done else "•"
        color = "green" if t.done else "yellow"
        table.add_row(str(t.id), f"[{color}]{icon}[/{color}]", t.description)
    console.print(table)

@app.command(name="undone")
def mark_undone(task_id: int):
    service = get_service()
    updated = service.mark_undone(task_id)
    if updated:
        console.print(f"[yellow]Marked as not done:[/yellow] {updated.description} (ID: {updated.id})")
    else:
        console.print(f"[red]Task with ID {task_id} not found[/red]")

@app.command()
def purge():
    service = get_service()
    count = service.purge()
    console.print(f"[red]Purged {count} tasks (all deleted)[/red]")

@app.command(name="upd")
def update(task_id: int, description: str):
    service = get_service()
    updated = service.update_task(task_id, description)
    if updated:
        console.print(f"[blue]Updated:[/blue] {updated.description} (ID: {updated.id})")
    else:
        console.print(f"[red]Task with ID {task_id} not found[/red]")
