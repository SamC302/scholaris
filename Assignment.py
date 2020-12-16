from Grades import Grade


class Assignment:
    def __init__(self, points_string, category, name, real=True):
        if '/' in points_string:
            points, t_points = points_string.strip().split(' / ')
            graded = True
        else:
            points = 0
            t_points = points_string.split(' ')[0]
            graded = False

        self.points = float(points)
        self.total_points = float(t_points)
        self.category = category
        self.name = name
        self.real = real
        self.modified = False
        self.graded = graded

    def set_total_points(self, val):
        self.modified = True
        self.total_points = val

    def set_points(self, val):
        self.modified = True
        self.graded = True
        self.points = val

    def set_category(self, val):
        self.modified = True
        self.category = val

    def get_percentage(self):
        return round(self.points / self.total_points, 2)

    def get_grade(self):
        p = self.get_percentage()
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

    def get_points_string(self):
        if self.graded:
            return f'{self.points} / {self.total_points}'
        else:
            return f'{self.total_points} points possible'

    def __str__(self):
        if self.graded:
            return f'On {self.name} (in {self.category}), you received a {self.points} out of {self.total_points} which is an {self.get_grade()} '


