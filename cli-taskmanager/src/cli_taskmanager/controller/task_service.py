from typing import List, Optional
from cli_taskmanager.model.task import Task
from cli_taskmanager.storage.sqlite_storage import SQLiteStorage

class TaskService:
    def __init__(self):
        self.storage = SQLiteStorage()

    def add_task(self, description: str) -> Task:
        task_id = self.storage.add_task(description)
        return self.storage.get_task(task_id)

    def mark_done(self, task_id: int) -> Optional[Task]:
        self.storage.mark_done(task_id)
        return self.storage.get_task(task_id)

    def delete_task(self, task_id: int) -> bool:
        task = self.storage.get_task(task_id)
        if not task:
            return False
        self.storage.delete_task(task_id)
        return True

    def clear_done(self) -> int:
        done_tasks = self.storage.list_tasks(status="done")
        self.storage.clear_done()
        return len(done_tasks)

    def list_tasks(self, status: str = "all") -> List[Task]:
        return self.storage.list_tasks(status=status)

    def mark_undone(self, task_id: int) -> Optional[Task]:
        self.storage.mark_undone(task_id)
        return self.storage.get_task(task_id)

    def purge(self) -> int:
        all_tasks = self.storage.list_tasks(status="all")
        self.storage.purge()
        return len(all_tasks)

    def update_task(self, task_id: int, description: str) -> Optional[Task]:
        self.storage.update_task(task_id, description)
        return self.storage.get_task(task_id)
