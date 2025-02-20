# RoadmapSh Task Tracker Project

Description: https://roadmap.sh/projects/task-tracker

**Developer notes**: No external libraries are used to run (but `json` & `datetime` are standard library thus IMO acceptable)
and while `pytest` & `ruff` are (optional) external libraries, they are used for testing / linting, not required to run

How to run:

`main.py <operation> <param1> <param2>`

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