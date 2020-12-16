from Assignment import Assignment


class Courses:
    def __init__(self, categories, weights, assignments=None):
        if assignments is None:
            assignments = []
        self.assignments = assignments
        self.categories = categories
        self.category_weights = {c: w for c, w in zip(categories, weights)}
        self.category_grades = {}
        self.total_grade = None
        self.total_grade_letter = None

    def add_assignment(self,assignment):
        self.assignments.append(assignment)
        self.calculate_grade()

    def calculate_grade(self):
        for category in self.categories:
            points_sum = sum([a.points for a in self.assignments if a.category == category])
            total_points_sum = sum([sum([a.total_points for a in self.assignments if a.category == category])])
            self.category_grades[category] = [points_sum,total_points_sum,points_sum/total_points_sum]
        self.total_grade = sum([self.category_weights[category]*self.category_grades[category][2] for category in self.categories])

