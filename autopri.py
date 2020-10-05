#!/usr/bin/env python3
import os
import sys
import math
from datetime import datetime, timedelta
import re

# for finding if a priority
# match = re.search(r"\s\(([A-Z])\)\s", task)


def main(todo_file, days=1, pri="A"):
    """
    Reprioritise tasks to **pri** if current date is **days** before due date.
    Will not reprioritise tasks if they are already higher priority than **pri**.
    Argument: todo_file
        The path to the todo.txt file
    Argument: days (default: 1)
        Number of days in advance of due date to be considered for reprioritising
    Argument: pri (default: "A")
        Priority to make tasks that need repriroritising
    """
    days = int(days)
    tasks_with_due_date = []

    # Open todo.txt file
    with open(todo_file, "r") as f:
        content = f.readlines()
        date = datetime.today()

        # Loop through content and look for due dates, assuming standard date format
        due_key = os.getenv("TODO_TXT_DUE_KEY", "due")

        for i, task in enumerate(content):
            match = re.findall(r"%s:(\d{4}-\d{2}-\d{2})" % due_key, task)

            if match:
                date = datetime.strptime(match[0], "%Y-%m-%d").date()
                tasks_with_due_date.append((i, task, date))

    # get taks within set days
    tasks_within_days = []
    for task in tasks_with_due_date:
        if task[2] < datetime.today().date() + timedelta(days+1):
            tasks_within_days.append(task)

    # basic output
    tasks_to_print = []
    zero_pad = int(math.log10(len(content))) + 1
    for task in tasks_within_days:
        tasks_to_print.append(str(task[0] + 1).zfill(zero_pad) + " " + task[1])
    # Print to console
    if len(tasks_to_print) > 0:
        print("\n===================================")
        print("Tasks within days:")
        print("===================================")
        for task in tasks_to_print:
            print(task)


if __name__ == "__main__":
    # check all inputs as expected and pass to main script
    if (len(sys.argv) < 2) or (len(sys.argv) > 4):
        print("Usage: autopri.py [TODO_FILE] <days> <priority>")
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print(f"Error: {sys.argv[1]} is not a file")
        sys.exit(1)

    if len(sys.argv) == 4:
        if not str.isdigit(sys.argv[2]):
            print(f"Error: days argument '{sys.argv[2]}' is not an integer")
            sys.exit(1)
        if len(sys.argv[3]) > 1:
            print(f"Error: priority argument '{sys.argv[3]}' should only be one letter")
            sys.exit(1)
        if not str.isalpha(sys.argv[3]):
            print(f"Error: priority argument '{sys.argv[3]}' is not a letter")
            sys.exit(1)

        main(sys.argv[1], sys.argv[2], sys.argv[3])
        sys.exit(0)

    if len(sys.argv) == 3:
        if not str.isdigit(sys.argv[2]) and (len(sys.argv[2]) > 1):
            print(f"Error: priority argument '{sys.argv[2]}' should only be one letter")
            sys.exit(1)

        if str.isalpha(sys.argv[2]) and (len(sys.argv[2]) == 1):
            main(sys.argv[1], pri=sys.argv[2])
            sys.exit(0)

        if str.isdigit(sys.argv[2]):
            main(sys.argv[1], days=sys.argv[2])
            sys.exit(0)

    main(sys.argv[1])
