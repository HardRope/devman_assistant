from collections import Counter
from math import ceil

from team_projects.models import (AvailableTimecode, Group, Level, Project,
                                  Student, Timecode)

from .db_processing import get_timecodes_buttons

PROJECT = Project.objects.all()[0]
STUDENT = Student.objects.all()[0]


def sort_students(project: Project = PROJECT):
    available_timecodes = project.available_timecodes.all()
    students_timecodes = Timecode.objects.filter(project=project).order_by('timecode')
    
    groups = {
        timecode: {'level': None, 'students': []}
        for timecode
        in available_timecodes
    }

    assert isinstance(groups, dict) and len(groups) == len(available_timecodes)

    all_students = {
        student: [
            timecode.timecode
            for timecode
            in students_timecodes
            if timecode.student == student
        ]
        for student
        in project.students.all()
    }
    seniors = {
        student: [
            timecode.timecode
            for timecode
            in students_timecodes
            if timecode.student == student
        ]
        for student
        in project.students.all()
        if student.level.title == 'senior'
    }
    not_seniors = {
        student: [
            timecode.timecode
            for timecode
            in students_timecodes
            if timecode.student == student
        ]
        for student
        in project.students.all()
        if student.level.title != 'senior'
    }

    groups_for_senior = ceil(len(seniors) / 3)
    
    min_timecodes = 100
    for student, timecodes in all_students.items():
        if min_timecodes < len(timecodes):
            min_timecodes = len(timecodes)
    
    min_timecodes_senior = {
        student: timecode 
        for student, timecode 
        in all_students.items() 
        if len(timecodes) == min_timecodes 
        and student.level.title == 'senior'
    }
    
    if len(min_timecodes_senior) > groups_for_senior:
        seniors_timecodes = counter_timecodes(seniors)

        temp = dict()
        for student, timecode in min_timecodes_senior:
            temp.update({timecode: seniors_timecodes[timecode]})

        sorted_seniors_timecodes = sort_counter_timecodes_max2min(temp)
        senior_available_timecodes = sorted_seniors_timecodes[:groups_for_senior]
    else:
        сountered_timecodes = counter_timecodes(seniors)
        sorted_seniors_timecodes = sort_counter_timecodes_max2min(сountered_timecodes)
        
        senior_available_timecodes = list()
        for timecode, _ in sorted_seniors_timecodes.items():
            senior_available_timecodes.append(timecode)
    
    seniors, groups = sort_them(seniors, senior_available_timecodes[:2], groups)
    
    not_seniors, groups = sort_them(not_seniors, available_timecodes, groups)
    
    students = dict()
    students.update(seniors)
    students.update(not_seniors)
    
    students, groups = try_to_sort_unsorted(students, groups, project, all_students)
    students, groups = try_to_replace_groups(students, groups, project, all_students)
    
    for timecode, info in groups.items():
        print('-' * 20)
        print(timecode)
        print(info['level'])
        print(info['students'])

    necessary_timecodes = [
        timecode 
        for timecode, groups_info 
        in groups.items() 
        if len(groups_info["students"]) < 3
    ]
    
    print(f'\n{"-" * 20}\nUNSORTED STUDENTS')
    for student in students:
        print(student, student.level.title, students[student])
        ask_for_extra_timecode(student, necessary_timecodes, project)    
    
    return groups, students


def try_to_sort_unsorted(students, groups, project, all_students):
    temporary_students = dict()
    for timecode in groups:
        current_students = groups[timecode]['students']
        if len(current_students) == 1:
            temporary_students[current_students[0]] = all_students[current_students[0]]
            groups[timecode]['students'].clear()
            groups[timecode]['level'] = None
    if temporary_students: 
        available_timecodes = project.available_timecodes.all()
        students, groups = sort_them(students, available_timecodes, groups)
        students.update(temporary_students)
        students, groups = sort_them(students, available_timecodes, groups)
    return students, groups


def try_to_replace_groups(_students, _groups, project, all_students):
    sorted_timecodes = sort_counter_timecodes_max2min(
        counter_timecodes(_students)
    )
    groups = dict()
    for group, info in _groups.items():
        groups[group] = info

    students = dict()
    for student, info in students.items():
        students[student] = info

    temporary_students = dict()
    for timecode, number in sorted_timecodes.items():
        current_students = groups[timecode]['students']
        if number <= len(current_students):
            continue
        for student in current_students:
            temporary_students[student] = all_students[student]
        groups[timecode]['students'].clear()
        groups[timecode]['level'] = None
    if not temporary_students:
        return _students, _groups
    available_timecodes = project.available_timecodes.all()
    students, groups = sort_them(students, available_timecodes, groups)
    students.update(temporary_students)
    students, groups = sort_them(students, available_timecodes, groups)
    if _students <= students:
        return _students, _groups
    else:
        return students, groups


def counter_timecodes(students: dict) -> Counter:
    students_timecodes = []
    for _, timecodes in students.items():
        students_timecodes += timecodes
    return Counter(students_timecodes)


def sort_counter_timecodes_max2min(timecodes: dict) -> dict():
    sorted_students_timecodes = dict()
    for value in sorted(timecodes.values(), reverse=True):
        for key in timecodes.keys():
            if timecodes[key] == value:
                sorted_students_timecodes[key] = value
    return sorted_students_timecodes


def sort_them(students, available_timecodes, groups):
    for num, timecode in enumerate(available_timecodes):
        if num < -3:
            suitable_students = [
                {'student': student, 'timecodes':timecodes}
                for student, timecodes
                in students.items()
                if len(timecodes) == num + 1
            ]
        else:
            suitable_students = [
                {
                    'student': student,
                    'timecodes':timecodes
                }
                for student, timecodes
                in students.items()
                if timecode in timecodes
            ]

        processed_students = list()
        
        for student in suitable_students:
            group_level = groups[timecode]['level']
            student_level = student['student'].level

            if group_level is None and student_level.title in ('junior', 'middle'):
                groups[timecode]['level'] = student_level
            elif group_level is None and student_level.title == 'senior':
                groups[timecode]['level'] = student_level

            is_compatible = check_level_compatible(group_level, student_level)
            in_group = len(groups[timecode]['students'])
            
            if is_compatible and in_group < 3:
                groups[timecode]['students'].append(student['student'])
                processed_students.append(student)
        
        for student in processed_students:
            students.pop(student['student'])
    return students, groups


def check_level_compatible(level1: Level, level2: Level) -> bool:
    try:
        return (
            (
                level1.title in ('junior', 'middle')
                and level2.title in ('junior', 'middle')
            )
            or
            (
                level1.title == 'senior'
                and level2.title == 'senior'
            )
        )
    except AttributeError:
        return True


# from .bot import ask_for_timecode
def ask_for_extra_timecode(student: Student,
                           necessary_timecodes: list,
                           project: Project):
    buttons = get_timecodes_buttons(student, project)

    #ask_for_timecode(student, necessary_timecodes, buttons)