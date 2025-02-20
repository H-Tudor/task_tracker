from datetime import datetime
import os
import pathlib
import pytest

from ..models import Task, TaskStatus
from .. import TaskService


@pytest.fixture()
def task_sample():
    now = datetime.now()
    yield Task(1, "Hello, World!", TaskStatus.TODO, now, now)


@pytest.fixture()
def service():
    _service = TaskService("test.json")

    yield _service

    if os.path.exists(_service.file):
        pathlib.Path.unlink(_service.file)
