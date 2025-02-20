from enum import Enum
from src.task import TaskService
from src.task.models import Task, TaskStatus


class CliColors(Enum):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class TaskCli:
    def __init__(self, file: str):
        self.service = TaskService(file)
        self.handlers = {
            "add": self.handle_add,
            "update": self.handle_update,
            "delete": self.handle_delete,
            "mark_in_progress": self.handle_mark_in_progress,
            "mark_done": self.handle_mark_done,
            "list": self.handle_list,
        }

    def run(self, args: list[str]) -> None:
        if len(args) == 0:
            return self.print("No args provided", CliColors.WARNING)

        if args[0] not in self.handlers.keys():
            return self.print(f"Unknown operation '{args[0]}'", CliColors.FAIL)

        return self.handlers[args[0]](args)

    def print(self, message, color: CliColors | None = None) -> None:
        print((color.value if color else "") + message + CliColors.ENDC.value)

    def handle_add(self, args: list[str]) -> None:
        if len(args) == 1:
            return self.print("Missing Task Description", CliColors.FAIL)

        if len(args) > 2:
            self.print(f"Everything after '{args[1]}' is ignored", CliColors.WARNING)

        self.print(f"Task added successfully (ID: {self.service.add(args[1]).id})")

    def handle_update(self, args: list[str]) -> None:
        if len(args) < 3:
            return self.print(
                (
                    "Missing Task Id & Description"
                    if len(args) == 1
                    else "Missing Task Description"
                ),
                CliColors.FAIL,
            )

        if not args[1].isdigit() or int(args[1]) <= 0:
            return self.print("The provided task id is not valid", CliColors.FAIL)

        if len(args) > 3:
            self.print(f"Everything after '{args[2]}' is ignored", CliColors.WARNING)

        result = self.service.update(int(args[1]), args[2])
        if not result:
            return self.print("Task could not be updated", CliColors.FAIL)

        self.print("Task updated successfully")

    def handle_delete(self, args: list[str]) -> None:
        if len(args) == 1:
            return self.print("Missing Task Id", CliColors.FAIL)

        if not args[1].isdigit() or int(args[1]) <= 0:
            return self.print("The provided task id is not valid", CliColors.FAIL)

        if len(args) > 2:
            self.print(f"Everything after '{args[1]}' is ignored", CliColors.WARNING)

        result = self.service.delete(int(args[1]))
        if not result:
            return self.print("Task could not be deleted", CliColors.FAIL)

        self.print("Task updated deleted")

    def handle_mark_in_progress(self, args: list[str]) -> None:
        if len(args) == 1:
            return self.print("Missing Task Id", CliColors.FAIL)

        if not args[1].isdigit() or int(args[1]) <= 0:
            return self.print("The provided task id is not valid", CliColors.FAIL)

        result = self.service.mark_in_progress(int(args[1]))
        if not result:
            return self.print("Task could not be updated", CliColors.FAIL)

        self.print(f"Task moved to in-progress (ID: {result.id})", CliColors.OKCYAN)

    def handle_mark_done(self, args: list[str]) -> None:
        if len(args) == 1:
            return self.print("Missing Task Id", CliColors.FAIL)

        if not args[1].isdigit() or int(args[1]) <= 0:
            return self.print("The provided task id is not valid", CliColors.FAIL)

        result = self.service.mark_done(int(args[1]))
        if not result:
            return self.print("Task could not be updated", CliColors.FAIL)

        self.print(f"Task moved to done (ID: {result.id})", CliColors.OKGREEN)

    def handle_list(self, args: list[str]) -> None:
        data = (
            self.service.list(TaskStatus[Task.covert_status(args[1], False)])
            if len(args) > 1
            else self.service.list()
        )

        print(
            f"Tasks:\n\t{'CreatedAt(20)':{' '}^20} {'Id(4)':{' '}^4} {'Status(12)':{' '}^12} {"Title(30)":{' '}^30} {'Updated At'}"
        )
        for task in data:
            color = None
            if task.status is TaskStatus.DONE:
                color = CliColors.OKGREEN
            elif task.status is TaskStatus.IN_PROGRESS:
                color = CliColors.OKCYAN

            self.print(str(task), color)
