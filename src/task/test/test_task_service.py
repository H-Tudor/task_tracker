import json
import os
from time import sleep
from .. import TaskService
from ..models import Task, TaskStatus
from . import task_sample, service

_ = [task_sample, service]


def test_add(task_sample: Task, service: TaskService):
    actual = service.add(task_sample.description)
    assert actual is not None
    assert isinstance(actual, Task)
    assert actual.id == 1
    assert actual.description == task_sample.description
    assert actual.status == task_sample.status
    assert actual.created_at == task_sample.created_at
    assert actual.updated_at == task_sample.updated_at

    actual = service.add(task_sample.description)
    assert actual.id == 2


def test_update(task_sample: Task, service: TaskService):
    service.add(task_sample.description)
    service.add(task_sample.description)
    control = "Test"
    sleep(1)

    actual = service.update(2, control)
    assert actual is not None
    assert isinstance(actual, Task)
    assert actual.description == control
    assert actual.created_at != actual.updated_at


def test_update_missing(task_sample: Task, service: TaskService):
    control = "Test"

    actual = service.update(2, control)
    assert actual is False


def test_delete(task_sample: Task, service: TaskService):
    service.add(task_sample.description)
    service.add(task_sample.description)

    actual = service.delete(1)
    assert actual is True


def test_delete_missing(task_sample: Task, service: TaskService):
    actual = service.delete(1)
    assert actual is False


def test_mark_in_progress(task_sample: Task, service: TaskService):
    service.add(task_sample.description)
    sleep(1)

    actual = service.mark_in_progress(1)
    assert actual is not None
    assert isinstance(actual, Task)
    assert actual.status == TaskStatus.IN_PROGRESS
    assert actual.created_at != actual.updated_at


def test_mark_in_progress_missing(task_sample: Task, service: TaskService):
    actual = service.mark_in_progress(1)
    assert actual is False


def test_mark_done(task_sample: Task, service: TaskService):
    service.add(task_sample.description)
    sleep(1)

    actual = service.mark_done(1)
    assert actual is not None
    assert isinstance(actual, Task)
    assert actual.status == TaskStatus.DONE
    assert actual.created_at != actual.updated_at


def test_mark_done_missing(task_sample: Task, service: TaskService):
    actual = service.mark_done(1)
    assert actual is False


def test_list(task_sample: Task, service: TaskService):
    service.add(task_sample.description)
    service.add(task_sample.description)
    service.add(task_sample.description)
    service.mark_in_progress(2)
    service.mark_done(3)

    actual = service.list()
    assert actual is not None
    assert isinstance(actual, list)
    assert len(actual) == 3

    actual = service.list(TaskStatus.TODO)
    assert actual is not None
    assert isinstance(actual, list)
    assert len(actual) == 1
    assert actual[0].id == 1


def test_save(task_sample: Task, service: TaskService):
    expected = [service.add(f"{x} -> {task_sample.description}") for x in range(3)]

    assert len(expected) == 3
    assert expected[-1].id == 3
    assert os.path.exists(service.file) and os.path.getsize(service.file) > 0
    with open(service.file) as f:
        assert f.read() == json.dumps([x.to_dict() for x in expected])


def test_load(task_sample: Task, service: TaskService):
    control = 3
    expected = [
        service.add(f"{x} -> {task_sample.description}") for x in range(control)
    ]

    assert len(expected) == control
    assert expected[-1].id == control
    assert os.path.exists(service.file) and os.path.getsize(service.file) > 0
    with open(service.file) as f:
        assert f.read() == json.dumps([x.to_dict() for x in expected])

    new_service = TaskService(service.file)
    actual = new_service.list()
    assert len(actual) == control
    assert actual[-1].id == control
    assert new_service.next_id == control + 1


def test_next_id(task_sample: Task, service: TaskService):
    control = 3
    expected = [
        service.add(f"{x} -> {task_sample.description}") for x in range(control)
    ]

    assert len(expected) == control
    assert expected[-1].id == control
    assert os.path.exists(service.file) and os.path.getsize(service.file) > 0
    with open(service.file) as f:
        assert f.read() == json.dumps([x.to_dict() for x in expected])

    service.delete(1)
    service.delete(2)
    new_service = TaskService(service.file)
    actual = new_service.list()
    assert len(actual) == 1
    assert actual[-1].id == control
    assert new_service.next_id == control + 1
