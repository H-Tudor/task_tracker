import pytest
from datetime import datetime
from ..models import Task, TaskStatus
from . import task_sample

_ = [task_sample]


def test_init():
    with pytest.raises(TypeError):
        Task()

    now = datetime.now().replace(microsecond=0)
    actual = Task(1, "Hello, World!", TaskStatus.TODO, now, now)

    assert actual is not None
    assert actual.id == 1
    assert actual.description == "Hello, World!"
    assert actual.status == TaskStatus.TODO
    assert actual.status.value == TaskStatus.TODO.value
    assert actual.created_at == now
    assert actual.updated_at == now


def test_validation():
    now = datetime.now()
    with pytest.raises(ValueError):
        Task.validate(None, "Hello, World!", TaskStatus.TODO, now, now)
        Task.validate(0, "Hello, World!", TaskStatus.TODO, now, now)
        Task.validate(-1, "Hello, World!", TaskStatus.TODO, now, now)
        Task.validate(1, None, TaskStatus.TODO, now, now)
        Task.validate(1, "", TaskStatus.TODO, now, now)
        Task.validate(1, "Hello, World!", None, now, now)
        Task.validate(1, "Hello, World!", 1, now, now)
        Task.validate(1, "Hello, World!", "1", now, now)
        Task.validate(1, "Hello, World!", TaskStatus.TODO, None, now)
        Task.validate(1, "Hello, World!", TaskStatus.TODO, "", now)
        Task.validate(1, "Hello, World!", TaskStatus.TODO, now, None)
        Task.validate(1, "Hello, World!", TaskStatus.TODO, now, "")


def test_to_dict(task_sample: Task):
    actual = task_sample.to_dict()

    assert actual is not None
    assert isinstance(actual, dict)
    assert actual["id"] == task_sample.id
    assert actual["description"] == task_sample.description
    assert actual["status"] == Task.covert_status(task_sample.status.name)
    assert actual["status"] == "todo"
    assert actual["createdAt"] == task_sample.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert (
        datetime.strptime(actual["createdAt"], "%Y-%m-%d %H:%M:%S")
        == task_sample.created_at
    )
    assert actual["updatedAt"] == task_sample.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    assert (
        datetime.strptime(actual["updatedAt"], "%Y-%m-%d %H:%M:%S")
        == task_sample.updated_at
    )


def test_from_dict(task_sample: Task):
    actual = Task.from_dict(task_sample.to_dict())

    assert actual is not None
    assert isinstance(actual, Task)
    assert actual.id == task_sample.id
    assert actual.description == task_sample.description
    assert actual.status == task_sample.status
    assert actual.created_at == task_sample.created_at
    assert actual.updated_at == task_sample.updated_at
