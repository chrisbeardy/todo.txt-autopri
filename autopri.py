#!/usr/bin/env python3
"""
A todo.sh addon for auto-prioritising tasks X days before they are due.
By default it will prioritise tasks that are due for the current day
or the next day to priority A.

This script should be called by the autopri bash script which passes in the
required arguments of the `main` function.
"""
import os
import sys
import getopt
import math
from datetime import datetime, timedelta
import re


def main(todo_file, todo_full_sh, days=1, pri="A", list_tasks=False):
    """
    Reprioritise tasks to **pri** if current date is **days** before due date.
    Will not reprioritise tasks if they are already higher priority than **pri**.
    Argument: todo_file
        The path to the todo.txt file
    Argument: todo_full_sh
        The path to the todo.sh file
    Argument: days (default: 1)
        Number of days in advance of due date to be considered for reprioritising
    Argument: pri (default: "A")
        Priority to make tasks that need reprioritising
    Argument: list_tasks (default: False)
        If True, lists tasks and asks for confirmation before reprioritising
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
            task = task.replace("\n", "")
            match = re.findall(r"%s:(\d{4}-\d{2}-\d{2})" % due_key, task)

            if match:
                date = datetime.strptime(match[0], "%Y-%m-%d").date()
                tasks_with_due_date.append((i+1, task, date))

    # only non completed tasks
    non_complete_tasks_with_due_date = []
    for task in tasks_with_due_date:
        if (task[1][0] == "x") and (task[1][1] == " "):
            continue
        non_complete_tasks_with_due_date.append(task)

    # get tasks within set days
    tasks_within_days = []
    for task in non_complete_tasks_with_due_date:
        if task[2] < datetime.today().date() + timedelta(days+1):
            tasks_within_days.append(task)

    # get tasks within priority
    tasks_within_pri = []
    for task in tasks_within_days:
        match = re.search(r"\(([A-Z])\)\s", task[1])
        if not match:
            tasks_within_pri.append(task)
        else:
            task_pri = task[1][1]
            if task_pri > pri:
                tasks_within_pri.append(task)

    repri_tasks = True
    if list_tasks:
        tasks_to_print = []
        zero_pad = int(math.log10(len(content))) + 1
        for task in tasks_within_pri:
            tasks_to_print.append(str(task[0]).zfill(zero_pad) + " " + task[1])
        # Print to console
        if len(tasks_to_print) > 0:
            print("Tasks to reprioritise")
            print("=====================\n")
            for task in tasks_to_print:
                print(task)
        while True:
            user_input = input("\nReprioritise tasks?(y/n)")
            if user_input == "y":
                break
            if user_input == "n":
                repri_tasks = False
                break

    if repri_tasks:
        for task in tasks_within_pri:
            os.system(todo_full_sh + " pri " + str(task[0]) + " " + pri)


if __name__ == "__main__":
    # check all inputs as expected and pass to main script
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "l", ["list"])
        list_tasks = False
        if len(opts) > 0:
            list_tasks = True
    except getopt.GetoptError:
        print("Error: option not valid")
        print("Usage: todo.sh -l <days> <priority>")
        sys.exit(1)

    if (len(args) < 2) or (len(args) > 4):
        print("Error: wrong number of parameters given")
        print("Usage: todo.sh -l <days> <priority>")
        sys.exit(1)

    if not os.path.isfile(args[0]):
        print(f"Error: todo file argument {args[0]} is not a file")
        print("Usage: autopri.py -l [TODO_FILE] [TODO_FULL_SH] <days> <priority>")
        sys.exit(1)

    if not os.path.isfile(args[1]):
        print(f"Error: todo.sh path argument {args[1]} is not a file")
        print("Usage: autopri.py -l [TODO_FILE] [TODO_FULL_SH] <days> <priority>")
        sys.exit(1)

    if len(args) == 4:
        if not str.isdigit(args[2]):
            print(f"Error: days argument '{args[2]}' is not an integer")
            print("Usage: todo.sh -l <days> <priority>")
            sys.exit(1)
        if len(args[3]) > 1:
            print(f"Error: priority argument '{args[3]}' should only be one letter")
            print("Usage: todo.sh -l <days> <priority>")
            sys.exit(1)
        if not str.isalpha(args[3]):
            print(f"Error: priority argument '{args[3]}' is not a letter")
            print("Usage: todo.sh -l <days> <priority>")
            sys.exit(1)

        main(args[0], args[1], args[2], args[3], list_tasks)
        sys.exit(0)

    if len(args) == 3:
        if not str.isdigit(args[2]) and (len(args[2]) > 1):
            print(f"Error: priority argument '{args[2]}' should only be one letter")
            print("Usage: todo.sh -l <days> <priority>")
            sys.exit(1)

        if str.isalpha(args[2]) and (len(args[2]) == 1):
            main(args[0], args[1], pri=args[2], list_tasks=list_tasks)
            sys.exit(0)

        if str.isdigit(args[2]):
            main(args[0], args[1], days=args[2], list_tasks=list_tasks)
            sys.exit(0)

    main(args[0], args[1], list_tasks=list_tasks)
