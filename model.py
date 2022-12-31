from datetime import datetime
from sqlite3 import Date


class Todo:
  def __init__(self, task_name: str, priority: str, created_date: Date, last_updated: Date = None, active_flag: str = 'Y'):
    self.task_name = task_name
    self.priority = priority
    self.created_date = datetime.now().isoformat()
    self.last_updated = last_updated
    self.active_flag = active_flag

  def __repr__(self) -> str:
    pass

