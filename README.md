# todo.txt-autopri

*A [todo.txt](https://github.com/ginatrapani/todo.txt-cli) addon for auto-prioritising tasks X days before they are due.*

By default it will prioritise tasks that are due for the current day or the next day to priority A.

It can be useful to set the command to run on shell startup or on a @daily cron job.

## Installation

1. Clone the repository:

`git clone https://github.com/chrisbeardy/todo.txt-autopri.git todo.txt-autopri`

2. Copy the autopri and autopri.py files into the actions directory, usually `$HOME/.todo.actions.d`
3. Make the files executable.

## Usage

*To auto-prioritise tasks based with the default parameters:*

`todo.sh autopri`

*Changing the number of days:*

The following will auto-prioritise tasks that are due in 3 days time to priority A:

`todo.sh autopri 3`

*Changing the priority:*

The following will auto-prioritise tasks that are due on the current day or in a days time to priority C:

`todo.sh autopri C`

*Changing both the number of days and the priority:*

The following will auto-prioritise tasks that are due in 3 days time to priority C:

`todo.sh autopri 3 C`

## Contributing

Please feel free to submit a PR for improvements.

## Thanks

Special thanks goes to the authors of the [due](https://github.com/rebeccamorgan/due) todo.txt addon whose python script I used as inspiration.
