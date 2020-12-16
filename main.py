import json

from rich.columns import Columns
from rich.panel import Panel

from Gradebook import Gradebook
from rich import print
from rich.prompt import Prompt, IntPrompt, Confirm
from studentvue import StudentVue
from Assignment import Assignment
import arrow
from rich.text import Text

from Grades import Grade
from terminal import console, grade_associate
from rich.table import Table
from rich.traceback import install

install(show_locals=True)


def getStudentVueData():
    username = IntPrompt.ask('Enter your user id')
    pwd = Prompt.ask('Enter your password')
    domain = 'https://md-mcps-psv.edupoint.com'
    remember = Confirm.ask('Do you want to be remembered?')
    studentvue_client = StudentVue(str(username), pwd, domain)
    while 'RT_ERROR' in studentvue_client.get_gradebook().keys():
        text = Text('Username or password is incorrect. Try again')
        text.stylize(style="red")
        console.print(text)
        username = IntPrompt.ask('Enter your user id')
        pwd = Prompt.ask('Enter your password')
        studentvue_client = StudentVue(str(username), pwd, domain)
    return studentvue_client.get_gradebook()


def print_grade_table(gradebook):
    table = Table(title="Grades")

    table.add_column("Course", justify="left")
    table.add_column('Percent')
    table.add_column('Letter')

    for course in gradebook.courses:
        grade_display = f'[{grade_associate[course.total_grade_letter]}]{gradebook.grades[course.title] * 100}%' if \
            gradebook.grades[course.title] else f'No Grade'
        letter_display = f'[{grade_associate[course.total_grade_letter]}]{course.total_grade_letter}' if course.total_grade_letter is not None else f'No Grade'
        table.add_row(course.title, grade_display, letter_display)
    console.print(
        Panel(
            Columns(
                (table,),
                align="center",
                expand=True
            ),
            title=f"[bold white]All Courses"
        )

    )

def course_commands(course):
    command = Prompt.ask(f"[blue bold]({course.title}) Enter a command")
    while True:
        if command == 'exit':
            return
        elif command == 'modify':
            grid = Table()
            grid.add_column('ID')
            grid.add_column('Assignment')
            count = 1
            for assignment in course.assignments:
                grid.add_row(str(count), assignment.name)
                count += 1
            console.print(grid)
            assignment_id = IntPrompt.ask("Enter the ID of the assignment you want to modify")
            property = Prompt.ask("What do you want to modify?",choices=["Points","Total Points","Category"])
            if property == 'Points':
                new_points = IntPrompt.ask("What should the new amount of points be?")
                course.assignments[assignment_id - 1].set_points(new_points)
            elif property == 'Total Points':
                new_points = IntPrompt.ask("What should the new amount of total points be?")
                course.assignments[assignment_id - 1].set_total_points(new_points)
            elif property == 'Category':
                grid = Table()
                grid.add_column('ID')
                grid.add_column('Category')
                count = 1
                for category in course.categories:
                    grid.add_row(str(count), category)
                    count += 1
                console.print(grid)
                category_id = IntPrompt.ask("What should the new category be?")
                course.assignments[assignment_id - 1].set_category(course.categories[category_id - 1])
            console.clear()
            course.calculate_grade()
            course.print_grade_table()
        elif command == 'reset':
            grid = Table()
            grid.add_column('ID')
            grid.add_column('Assignment')
            count = 1
            grid.add_row(str(0), 'All')
            for assignment in course.assignments:
                grid.add_row(str(count), assignment.name)
                count += 1
            console.print(grid)
            assignment_id = IntPrompt.ask("Enter the ID of the assignment you want to modify")
            if assignment_id == 0:
                for assignment in course.assignments:
                    assignment.reset()
            else:
                course.assignments[assignment_id - 1].reset()
            console.clear()
            course.calculate_grade()
            course.print_grade_table()
        else:
            print("[blue bold]({course.title}) [red]Invalid command!")
        command = Prompt.ask(f"[blue bold]({course.title}) Enter a command")
        console.clear()



def start_commands(gradebook):
    command = ''
    print('Welcome!')
    print('Enter "course" to select a course to view')
    command = Prompt.ask("Enter a command")
    while command.lower() != 'end':
        if command == 'course':
            grid = Table()
            grid.add_column('ID')
            grid.add_column('Course')
            count = 1
            for course in gradebook.courses:
                grid.add_row(str(count),course.title)
                count +=1
            console.print(grid)
            course_id = IntPrompt.ask("Enter the ID of the course you want to view")
            console.clear()
            gradebook.courses[course_id-1].print_grade_table()
            course_commands(gradebook.courses[course_id-1])
        else:
            print("[red]Invalid command!")
        command = Prompt.ask("Enter a command")
        console.clear()



def main():
    with open('file.json', 'r') as file:
        data = json.loads(file.read())

    refresh = False

    if (arrow.get(data['Last Time'], 'YYYY-MM-DD').date() < arrow.now('America/New_York').date()) or refresh:
        data = getStudentVueData()
        data['Last Time'] = arrow.utcnow().to('America/New_York').format('YYYY-MM-DD')
        with open('file.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    gradebook = Gradebook(data)
    print_grade_table(gradebook)

    start_commands(gradebook)

    for course in gradebook.courses:
        course.print_grade_table()


main()
