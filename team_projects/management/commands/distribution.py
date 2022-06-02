from team_projects.models import AvailableTimecode, Level, Student, Group, Project, Timecode
from django.db.models import Count
import json

PROJECT = Project.objects.all()[0]

def get_sorted_timecodes(project: Project = PROJECT) -> dict:
    students_timecodes = Timecode.objects.filter(project=project)
    sorted_timecodes = dict()
    for timecode in students_timecodes:
        level = timecode.student.level.__str__()
        time = timecode.timecode.converted()
        if level not in sorted_timecodes:
            sorted_timecodes.update({level: {}})
        if time not in sorted_timecodes[level]:
            sorted_timecodes[level].update({time: []})
        
        sorted_timecodes[level][time].append(timecode.student)
    return sorted_timecodes


def first_filter(level: Level, students: list, groups: list) -> list:
    current_level = [student for student in students if student[1] == level]
    if len(current_level) >= 3:
        return current_level[:3]


def test(project: Project = PROJECT):
    available_timecodes = project.available_timecodes.all()
    levels = Level.objects.all()
    students_timecodes = Timecode.objects.filter(project=project).order_by('timecode')
    summary_timecode_data = list()
    groups = list()
    for timecode in students_timecodes:
        summary_timecode_data.append(
            (
                timecode.timecode,
                timecode.student.level,
                timecode.student
            )
        )
    print('NON GROUPED STUDENTS')
    for student in summary_timecode_data:
        print(student)
    for timecode in available_timecodes:
        students = [student for student in summary_timecode_data if student[0]==timecode]
        for level in levels:
            new_group = first_filter(level, students, groups)
            if new_group is None:
                continue
            groups.append(new_group)
            for student in new_group:
                summary_timecode_data.remove(student)
            break
    
    for group in groups:
        print('-' * 20)
        for item in group:
            print(item)
    
    print('NON GROUPED STUDENTS')
    for student in summary_timecode_data:
        print(student)


def test2(project: Project = PROJECT):
    available_timecodes = project.available_timecodes.all()
    levels = Level.objects.all()
    students_timecodes = Timecode.objects.filter(project=project).order_by('student')
    
    groups = dict()
    for timecode in available_timecodes:
        groups.update({timecode.converted: []})
    
    sorted_students



def group_students(sorted_timecodes: dict = get_sorted_timecodes()):
    pass