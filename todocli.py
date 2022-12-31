import typer
from datetime import datetime
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all, get_by_id, update_task, insert_task, delete

console = Console()

console_info = Console(width=10)

app = typer.Typer()

@app.command()
def add(task: str, priority: str):
  console.print("Adding...", "white on green")
  todo = Todo(task, priority, datetime.now().isoformat(), None, None)
  insert_task(todo)
  console.print("Added!!", "white on green")
  show_all()

@app.command()
def delete_id(id: int):
  console.print("DELETING...", style="bold green")
  delete(id)
  show_all()

@app.command()
def update():
  print("make sure you enter exact field  name")
  field = input("Enter field you want to update (name, priority, active_flag): ")
  if field not in  ['name', 'priority', 'active_flag']:
    console.print()
    return
  field_value  = input("Enter field value: ")
  id = int(input('Enter Id: '))
  typer.echo(f'Updating id #{id}')
  update_task(id, field, field_value)
  show_all()

# @app.command()
# def complete(position: int):
#   typer.echo(f'Complete {position}')
#   show_all()

@app.command()
def show_all():
  console.print("SHOWING...\n\n\n", style="bold green")
  tasks = get_all() # Todo obj
  console.print("[bold magenta]Todos[/bold magenta]!")

  table = get_table_header()

  def get_category_color(category):
    COLORS = {'H': 'red', 'M': 'magenta', 'L': 'green'}
    if category in COLORS:
        return COLORS[category]
    return 'blue'

  if tasks:
    for idx, task in enumerate(tasks, start=1):
      c = get_category_color(task.priority)
      is_done_str = '❌' if task.active_flag == 'Y' else '✅'
      table.add_row(str(idx), task.task_name, f'[{c}]{task.priority}[/{c}]', is_done_str, task.created_date, task.last_updated )
  console.print(table)

# @app.command()
# def show_pending():
#   table = get_table_header()

#   # filter tasks that are completed!
#   # Final print them.
#   pass

# @app.command()
# def show_completed():
#   table = get_table_header()

#   # filter tasks that are completed!
#   # Final print them.
#   pass

def get_table_header() -> Table:
  
  table = Table(show_header=True, header_style="bold blue")
  table.add_column('#', style='dim')
  table.add_column("Name")
  table.add_column("Priority", justify="center")
  table.add_column("Active", justify="center")
  table.add_column("Created Date", justify="right")
  table.add_column("Last Updated", justify="right")


  return table


if __name__ == '__main__':
  app()