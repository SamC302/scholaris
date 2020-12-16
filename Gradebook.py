from Course import Course
from Assignment import Assignment


class Gradebook:
    def __init__(self,data):
        self.courses = []
        self.data = data
        self.grades = {}
        self.parse_data()

    def parse_data(self):
        courses = self.data['Courses']['Course']
        for course in courses:
            title = course['@Title']

            grade_data = course['Marks']['Mark']

            category_data = grade_data['GradeCalcularSummary']['AssignmentGradeCalc']
            categories = [c['@Type'] for c in category_data]
            weights = [c['@Weight'] for c in category_data]

            assignment_data = grade_data['Assignments']
            if assignment_data != {}:
                assignment_data = assignment_data['Assignment']
                assignments = [Assignment(a['@Score'],a['@Type'],a['@Measure']) for a in assignment_data]

            curr_Course = Course(title,categories,weights,assignments)
            self.courses.append(curr_Course)
            self.grades[curr_Course.title] = curr_Course.total_grade

