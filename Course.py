from rich.console import RenderGroup
from rich.panel import Panel

from terminal import console
from rich.columns import Columns
from rich.table import Table

from Assignment import Assignment
from Grades import Grade


class Course:
    def __init__(self, title, categories, weights, assignments=None):
        self.categories = [c for c in categories if c != 'TOTAL']
        self.category_weights = {c: w for c, w in zip(categories, weights)}
        self.category_grades = {}
        self.total_grade = None
        self.total_grade_letter = None
        self.title = title
        if assignments is None or assignments == []:
            self.assignments = []
        else:
            self.assignments = assignments
            self.calculate_grade()

    def add_assignment(self, assignment):
        self.assignments.append(assignment)
        self.calculate_grade()

    def calculate_grade(self):
        total_g = 0
        for category in self.categories:
            points_sum = sum([a.points for a in self.assignments if a.category == category and a.graded])
            total_points_sum = sum(
                [sum([a.total_points for a in self.assignments if a.category == category and a.graded])])
            if total_points_sum == 0:
                percent = None
            else:
                percent = points_sum / total_points_sum
            self.category_grades[category] = [points_sum, total_points_sum, percent]

            if percent is not None:
                a_categories = [a.category for a in self.assignments if a.graded]
                total_weight = sum(
                    [self.category_weights[category] for category in self.categories if category in a_categories])
                total_g += (self.category_weights[category] / total_weight) * self.category_grades[category][2]
        self.total_grade = total_g
        self.total_grade_letter = self.get_grade()

    def get_grade(self):
        p = self.total_grade
        if p >= Grade.A:
            return Grade.A
        elif p >= Grade.B:
            return Grade.B
        elif p >= Grade.C:
            return Grade.C
        elif p >= Grade.D:
            return Grade.D
        elif p >= Grade.E:
            return Grade.E
        else:
            return None

    def get_category_grade(self, category):
        try:
            p = self.category_grades[category][2]
        except KeyError as e:
            return Grade.NOGRADE
        if p is None:
            return Grade.NOGRADE
        if p >= Grade.A:
            return Grade.A
        elif p >= Grade.B:
            return Grade.B
        elif p >= Grade.C:
            return Grade.C
        elif p >= Grade.D:
            return Grade.D
        elif p >= Grade.E:
            return Grade.E
        else:
            return None

    def print_grade_table(self):
        grade_associate = {
            Grade.A: 'bold green',
            Grade.B: 'bold yellow',
            Grade.C: 'bold blue',
            Grade.D: 'bold red',
            Grade.E: 'bold white',
            Grade.NOGRADE: ''
        }

        p_table = Table(title=f"Overall Grade", show_footer=True)
        p_table.add_column("Category", footer="Total")
        p_table.add_column("Weight", footer="100%")
        if self.total_grade is not None:
            p_table.add_column("Percent",
                               footer=f'[{grade_associate[self.total_grade_letter]}]{round(self.total_grade, 4) * 100}%')
        else:
            p_table.add_column("Percent",
                               footer=f'No Grade')
        if self.total_grade_letter is not None:
            p_table.add_column("Grade", f'[{grade_associate[self.total_grade_letter]}]{self.total_grade_letter}')
        else:
            p_table.add_column("Grade",
                               footer=f'No Grade')

        for category in self.categories:
            if category in self.category_grades.keys() and self.category_grades[category][2] is not None:
                grade_display = f'[{grade_associate[self.get_category_grade(category)]}]{round(self.category_grades[category][2], 4) * 100}%'
            else:
                grade_display = f'No Grade'
            if category in self.category_grades.keys() and self.category_grades[category][2] is not None:
                letter_display = f'[{grade_associate[self.get_category_grade(category)]}]{self.get_category_grade(category)}'
            else:
                letter_display = f'No Grade'
            p_table.add_row(category, f'{round(self.category_weights[category], 4) * 100}%', grade_display,
                            letter_display)

        table = Table(title=f"Assignments")

        table.add_column("Assignment", justify="left")
        table.add_column("Category")
        table.add_column("Points")
        table.add_column('Percent')
        table.add_column('Letter')

        for assignment in self.assignments:
            grade_display = f'[{grade_associate[assignment.get_grade()]}]{assignment.get_percentage() * 100}%' if \
                assignment.graded else f'No Grade'
            letter_display = f'[{grade_associate[assignment.get_grade()]}]{assignment.get_grade()}' if assignment.graded else f'No Grade'
            points_display = f'[{grade_associate[assignment.get_grade()]}]{assignment.get_points_string()}' if assignment.graded else f'{assignment.get_points_string()}'
            table.add_row(assignment.name, assignment.category, points_display, grade_display, letter_display)

        console.print(
            Panel(
                Columns(
                    (table, p_table),
                    align="center",
                    expand=True,
                    title=f"[white bold]{self.title}"))
        )
