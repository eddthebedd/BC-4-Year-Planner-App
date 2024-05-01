from planner.models import Planner, Student
import json


def validateMajor(planner: Planner, student: Student):
    majors = [student.major_one, student.major_two]
    minors = [student.minor_one, student.minor_two]
    for i, major in enumerate(majors):
        if major is not None:
            majors[i] = major.id
    for i, minor in enumerate(minors):
        if minor is not None:
            minors[i] = minor.id
    courses = pull_courses(planner)
    validator = {}
    with open('planner/degree_audit.json') as f:
        data = json.load(f)
        for major in majors:
            if major is not None:
                majorKey = f'{str(major).upper()} Major'
                unfulfilled, remaining = check_specific(courses, data['Majors'][major]['specific'])
                validator[majorKey] = {'Unfulfilled Requirements': unfulfilled}   
                electives, remaining = check_additional(remaining, data['Majors'][major]['additional'])           
                validator[majorKey]['Unfulfilled Electives'] = electives
                print(validator)
        for minor in minors:
            if minor is not None:
                minorKey = f'{minor} Minor'
                unfulfilled, remaining = check_specific(courses, data['Minors'][minor]['specific'])
                validator[minorKey] = {'Unfulfilled Requirements': unfulfilled}
                electives, remaining = check_additional(remaining, data['Minors'][minor]['additional'])
                validator[minorKey]['Unfulfilled Electives'] = electives
    return validator


def check_specific(courses: dict, spec: dict):
    for item in courses.copy():
        if item in spec:
            courses.remove(item)
            spec.remove(item)
    
    return spec, courses
   

def check_additional(courses: dict, add: dict):
    taken_electives = {}
    for add_ in add:
        num, level = parse_additional(add_)
        for course in courses.copy():
            if course[4:].startswith(level):
                courses.remove(course)
                num -= 1

        if num > 0:
            taken_electives[int(level) * 1000] = number_to_word(num)
    return taken_electives, courses


def parse_additional(add: str):
    num, level = add.split('.')
    return int(num), level


def pull_courses(planner: Planner):
    planner.semesters = [
                ('fall_one', planner.fall_one),
                ('spring_one', planner.spring_one),
                ('fall_two', planner.fall_two),
                ('spring_two', planner.spring_two),
                ('fall_three', planner.fall_three),
                ('spring_three', planner.spring_three),
                ('fall_four', planner.fall_four),
                ('spring_four', planner.spring_four),
            ]
    return [course.id for semester in planner.semesters for course in semester[1].courses.all()]

def number_to_word(number):
    return  {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
             6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
             }.get(number)