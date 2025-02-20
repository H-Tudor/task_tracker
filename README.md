# RoadmapSh Task Tracker Project

This is a solution submission for the Task Tracker (beginner) project from [Roadmap.sh](https://roadmap.sh)

The full project requirements can be found at: https://roadmap.sh/projects/task-tracker

## Features

As described in the above link, this application implements the CRUD operations on the Task Entity and persists 
data in a JSON file.

The CRUD operations are:
- create
- list all
- list by status
- update description
- update status
- delete by id

With this project I focused on
- organizing the project as a modular monolith which allows
    - forward extensibility for an eventual REST API
    - isolation of different concerns
- implementing unit tests of each functionality (model, service, console-interface)
- CLI user experience (with Jira-like colors for task statuses) and tabular listing using padding
- making an installable application

## Constraints

This project did not allow usage of external libraries & frameworks and enforced data persistence in a JSON file

**Developer notes**:
- No external libraries are used to run (but `json` & `datetime` are standard library thus IMO acceptable)
- For development, the UV package / project manager was used along side pytest for unit-testing and ruff for linting & formatting 
- If not for the above constraints, I would have used Typer and SqlModel
- data I/O was implemented by the described interface, but internally I used a slight variation on names

## How to run:

```
pip install https://github.com/H-Tudor/task_tracker
task add "Title"
```

Where operations:
- add
    - param1: description
    - param2: N/A
- update
    - param1: id 
    - param2: description
- delete
    - param1: id
    - param2: N/A
- mark-in-progress
    - param1: id
    - param2: N/A
- mark-done
    - param1: id
    - param2: N/A
- list
    - param1: status (`<empty>`, `todo`, `in-progress`, `done`)
    - param2: N/A
