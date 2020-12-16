import json
from Gradebook import Gradebook
from rich import print
from studentvue import StudentVue

with open('file.json', 'r') as file:
    data = json.loads(file.read())

s = StudentVue(input('user:'),input('password:'))

g = Gradebook(data)
print(g.grades)
