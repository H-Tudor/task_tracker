from datetime import datetime
import os
import pathlib
import pytest

from .. import TaskService
from ..cli import TaskCli
from ..models import Task, TaskStatus


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


@pytest.fixture()
def cli():
    _cli = TaskCli("test.json")

    yield _cli

    if os.path.exists(_cli.service.file):
        pathlib.Path.unlink(_cli.service.file)
