import os
import json
import inspect
import pathlib
from datetime import datetime

from .models import Task, TaskStatus


class TaskService:
    def __init__(self, filename: str):
        self.file = (
            pathlib.Path(inspect.stack()[-1].filename).parent.absolute()
            / pathlib.Path(filename).name
        )
        self.data: dict[int, Task] = {}
        self.next_id = 1
        self.load_data()

    def add(self, description: str) -> Task:
        now = datetime.now()
        task = Task(self.next_id, description, TaskStatus.TODO, now, now)
        self.data[self.next_id] = task
        self.next_id += 1
        self.save_data()

        return task

    def update(self, id: int, description: str) -> Task | bool:
        if id not in self.data.keys():
            return False

        self.data[id].description = description
        self.data[id].updated_at = datetime.now()
        self.save_data()
        return self.data[id]

    def delete(self, id: int) -> bool:
        if id not in self.data.keys():
            return False

        self.data.pop(id)
        self.save_data()
        return True

    def mark_in_progress(self, id: int) -> Task | bool:
        if id not in self.data.keys():
            return False

        self.data[id].status = TaskStatus.IN_PROGRESS
        self.data[id].updated_at = datetime.now()
        self.save_data()
        return self.data[id]

    def mark_done(self, id: int) -> Task | bool:
        if id not in self.data.keys():
            return False

        self.data[id].status = TaskStatus.DONE
        self.data[id].updated_at = datetime.now()
        self.save_data()
        return self.data[id]

    def list(self, status: TaskStatus | None = None) -> list[Task]:
        return [x for x in self.data.values() if not status or x.status == status]

    def load_data(self):
        if len(self.data) > 0:
            self.save_data()

        if not os.path.exists(self.file) or os.path.getsize(self.file) == 0:
            return {}

        with open(self.file) as f:
            tasks = [Task.from_dict(x) for x in json.load(f)]
            self.data = {x.id: x for x in tasks}
            self.next_id = tasks[-1].id + 1

    def save_data(self):
        with open(self.file, mode="w", encoding="utf-8") as f:
            json.dump([x.to_dict() for x in self.data.values()], f)
