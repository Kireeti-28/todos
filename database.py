import sqlite3
from model import Todo
from typing import List
from rich.console import Console
from datetime import datetime
import sys, traceback

conn = sqlite3.connect('tracker1.db')

cursor = conn.cursor()

console = Console()

def create_table():
  cursor.execute("""
    create table if not exists todos (
      task_name text,
      priority text,
      created_date text,
      last_updated text,
      active_flag text
    )"""
  )

create_table()

def pretty_error(er):
  print('SQLite error: %s' % (' '.join(er.args)))
  print("Exception class is: ", er.__class__)
  print('SQLite traceback: ')
  exc_type, exc_value, exc_tb = sys.exc_info()
  print(traceback.format_exception(exc_type, exc_value, exc_tb))

def insert_task(todo: Todo):
  try:
    with conn:
      cursor.execute("insert into todos values (:task_name, :priority, :created_date, :last_updated, :active_flag)",
      {'task_name': todo.task_name, 'priority': todo.priority, 'created_date': todo.created_date, 'last_updated': todo.last_updated, 'active_flag': todo.active_flag})
  except sqlite3.Error as er:
    pretty_error(er)



def update_task(id: int, field: str, field_value: str):
  try:
    with conn:
      if field == 'name':
        cursor.execute("update todos set task_name = :task_name, last_updated = :last_updated where rowid = :id", 
        {'task_name': field_value, 'last_updated': datetime.now().isoformat(), 'id': id})
      elif field == 'priority':
        cursor.execute("update todos set priority = :priority, last_updated = :last_updated where rowid = :id", 
        {'priority': field_value, 'last_updated': datetime.now().isoformat(), 'id': id})
      elif field == 'active_flag':
        cursor.execute("update todos set active_flag = :active_flag, last_updated = :last_updated where rowid = :id", 
        {'active_flag': field_value, 'last_updated': datetime.now().isoformat(), 'id': id})

  except sqlite3.Error as er:
    pretty_error(er)


def delete(id):
  try:
    with conn:
      cursor.execute("delete from todos where rowid = :id", {'id': id})

  except sqlite3.Error as er:
    pretty_error(er)


def get_by_id(id) -> Todo:
  try:
    cursor.execute("select * from todos where rowid = :id", {'id': id})
    result = cursor.fetchone()
    return Todo(*result)
  except sqlite3.Error as er:
    pretty_error(er)
    

def get_all() -> List[Todo]:
  try:
    cursor.execute("select * from todos")
    results = cursor.fetchall()
    todos = []
    if len(results) > 0:
      for res in results:
        todos.append(Todo(*res))
      return todos
    else:
      console.print("No data found.")

  except sqlite3.Error as er:
    pretty_error(er)

# def get_inactive() -> List[Todo]:
#   try:
#     cursor.execute("select * from todos where active_flag = 'N'")
#     results = cursor.fetchall()

#     inactive_todos = []
#     if len(results) > 0:
#       for res in results:
#         todo_obj = Todo(*res)
#         inactive_todos.append(todo_obj)
#       return inactive_todos
#     else:
#       console.print_exception('No inactive tasks were Found.')

#   except sqlite3.Error as er:
#     pretty_error(er)

  
# def get_active() -> List[Todo]:
#   try:
#     cursor.execute("select * from todos where active_flag = 'Y'")
#     results = cursor.fetchall

#     active_todos = []
#     if len(results) > 0:
#       for res in results:
#         todo_obj = Todo(*res)
#         active_todos.append(todo_obj)
#       return active_todos
#     else:
#       console.print_exception('No active tasks were Found.')

#   except sqlite3.Error as er:
#     pretty_error(er)







