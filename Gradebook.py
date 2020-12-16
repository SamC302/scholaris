from Course import Course
from Assignment import Assignment


class Gradebook:
    def __init__(self,data):
        self.courses = []
        self.data = data
        self.grades = {}
        self.parse_data()

    def parse_data(self):
        courses = self.data['Gradebook']['Courses']['Course']
        for course in courses:
            title = course['@Title']

            grade_data = course['Marks']['Mark']

            category_data = grade_data['GradeCalculationSummary']['AssignmentGradeCalc']
            categories = [c['@Type'] for c in category_data]
            weights = [float(c['@Weight'].strip('%'))/100 for c in category_data]

            assignment_data = grade_data['Assignments']
            if assignment_data != {}:
                assignment_data = assignment_data['Assignment']
                assignments = [Assignment(a['@Points'],a['@Type'],a['@Measure']) for a in assignment_data]
            else:
                assignments = []
            curr_course = Course(title,categories,weights,assignments)
            self.courses.append(curr_course)
            self.grades[curr_course.title] = round(curr_course.total_grade,4) if curr_course.total_grade is not None else curr_course.total_grade

    def get_course(self,name):
        for c in self.courses:
            if c.title == name:
                return c
        return None

    def update(self):
        for curr_course in self.courses:
            self.grades[curr_course.title] = round(curr_course.total_grade,
                                                   4) if curr_course.total_grade is not None else curr_course.total_grade


