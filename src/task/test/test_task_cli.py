from ..cli import TaskCli
from . import cli

_ = [cli]


def test_run(cli: TaskCli):
    assert cli.run([]) == 1
    assert cli.run(["x"]) == 2
    assert cli.run(["list"]) == 0


def test_add(cli: TaskCli):
    assert cli.run(["add"]) == 3

    result = cli.run(["add", "test"])
    assert result == 0
    result = cli.run(["add", "test2", "ignored"])
    assert result == 0


def test_update(cli: TaskCli):
    assert cli.run(["update"]) == 3
    assert cli.run(["update", "1"]) == 4
    assert cli.run(["update", "-1", "test"]) == 5
    assert cli.run(["update", "0", "test"]) == 5
    assert cli.run(["update", "1", "test"]) == 6

    cli.run(["add", "test"])
    assert cli.run(["update", "1", "test2", "ignored"]) == 0


def test_delete(cli: TaskCli):
    assert cli.run(["delete"]) == 3
    assert cli.run(["delete", "-1"]) == 4
    assert cli.run(["delete", "0"]) == 4
    assert cli.run(["delete", "1"]) == 5

    cli.run(["add", "test"])
    assert cli.run(["delete", "1", "ignored"]) == 0


def test_mark_in_progress(cli: TaskCli):
    assert cli.run(["mark_in_progress"]) == 3
    assert cli.run(["mark_in_progress", "-1"]) == 4
    assert cli.run(["mark_in_progress", "0"]) == 4
    assert cli.run(["mark_in_progress", "1"]) == 5

    cli.run(["add", "test"])
    assert cli.run(["mark_in_progress", "1", "ignored"]) == 0


def test_mark_done(cli: TaskCli):
    assert cli.run(["mark_done"]) == 3
    assert cli.run(["mark_done", "-1"]) == 4
    assert cli.run(["mark_done", "0"]) == 4
    assert cli.run(["mark_done", "1"]) == 5

    cli.run(["add", "test"])
    assert cli.run(["mark_done", "1", "ignored"]) == 0


def test_list(cli: TaskCli):
    cli.run(["add", "test"])
    cli.run(["add", "test"])
    cli.run(["add", "test"])
    cli.run(["mark_in_progress", "2"])
    cli.run(["mark_done", "3"])

    assert cli.run(["list"]) == 0
    assert cli.run(["list", "todo"]) == 0
    assert cli.run(["list", "todo", "ignored"]) == 0
    assert cli.run(["list", "test"]) == 1
