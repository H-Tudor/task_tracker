import sys

from src.task.cli import TaskCli


def main():
    try:
        TaskCli("data.json").run(sys.argv[1:])
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
