import click
import os
import json

tasks_file = "tasks.json"

def load_tasks():
    if os.path.exists(tasks_file):
        with open(tasks_file, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(tasks_file, 'w') as file:
        json.dump(tasks, file, indent=4)

@click.group()
def cli():
    """Simple task manager"""
    pass

@cli.command()
@click.argument('task')
def add(task):
    """Add a task"""
    tasks = load_tasks()
    tasks.append({"task":task, "completed":False})
    save_tasks(tasks)
    click.echo(f"Added task: {task}")

@cli.command()
def list():
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found.")
        return
    else:
        for index, task in enumerate(tasks, 1):
            status = "✅" if task["completed"] else "❌"
            click.echo(f"{index}. {task['task']} {status}")

@cli.command()
@click.argument('task_number', type=int)
def complete(task_number):
    """Mark a task as complete"""
    tasks = load_tasks()
    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as complete.")
    else:
        click.echo("Invalid task number.")

@cli.command()
@click.argument('task_number', type=int)
def delete(task_number):
    """Remove a task"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found.")
        return
    list()
    if 1 <= task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Removed task: {removed_task['task']}")
    else:
        click.echo("Invalid task number.")

if __name__ == '__main__':
    cli()