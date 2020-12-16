from Assignment import Assignment


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

    def add_assignment(self,assignment):
        self.assignments.append(assignment)
        self.calculate_grade()

    def calculate_grade(self):
        total_g = 0
        for category in self.categories:
            points_sum = sum([a.points for a in self.assignments if a.category == category and a.graded])
            total_points_sum = sum([sum([a.total_points for a in self.assignments if a.category == category and a.graded])])
            if total_points_sum == 0:
                percent = None
            else:
                percent = points_sum/total_points_sum
            self.category_grades[category] = [points_sum,total_points_sum,percent]

            if percent is not None:
                a_categories = [a.category for a in self.assignments if a.graded]
                total_weight = sum([self.category_weights[category] for category in self.categories if category in a_categories])
                total_g += (self.category_weights[category]/total_weight) * self.category_grades[category][2]
        self.total_grade = total_g

