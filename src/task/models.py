from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3


class Task:
    def __init__(
        self,
        id: int,
        description: str,
        status: TaskStatus,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.validate(id, description, status, created_at, updated_at)
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at.replace(microsecond=0)
        self.updated_at = updated_at.replace(microsecond=0)

    def __str__(self):
        return f"\t{self.updated_at.strftime("%Y-%m-%d %H:%M:%S"):{' '}<20} {self.id:{' '}>4} {self.covert_status(self.status.name):{' '}^12} {" ".join(self.description.split()[:5]):{' '}>30} {self.updated_at.strftime("%Y-%m-%d %H:%M:%S")}"

    @staticmethod
    def validate(
        id: int,
        description: str,
        status: TaskStatus,
        created_at: datetime,
        updated_at: datetime,
    ) -> bool:
        if not isinstance(id, int) or id <= 0:
            raise ValueError("Task Id has to be an integer greater than 0")

        if not isinstance(description, str) or len(description.strip()) == 0:
            raise ValueError("Task Description has to be a non-empty string")

        if not isinstance(status, TaskStatus):
            raise ValueError("Task Status has to be of type TaskStatus")

        if not isinstance(created_at, datetime):
            raise ValueError("Task Created At has to be of type datetime")

        if not isinstance(updated_at, datetime):
            raise ValueError("Task Updated At has to be of type datetime")

        return True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.covert_status(self.status.name),
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @classmethod
    def from_dict(cls, data: dict[str, int | str]):
        return cls(
            id=data["id"],
            description=data["description"],
            status=TaskStatus[cls.covert_status(data["status"], False)],
            created_at=datetime.strptime(data["createdAt"], "%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.strptime(data["updatedAt"], "%Y-%m-%d %H:%M:%S"),
        )

    @staticmethod
    def covert_status(status: str, out: bool = True):
        return (
            status.lower().replace("_", "-")
            if out
            else status.upper().replace("-", "_")
        )
