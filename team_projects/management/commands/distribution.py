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


def test(project: Project = PROJECT):
    available_timecodes = [timecode.time for timecode in AvailableTimecode.objects.all()]
    levels = [level.title for level in Level.objects.all()]
    students_timecodes = Timecode.objects.filter(project=project)
    for timecode in available_timecodes:
        for level in levels:
            students = [for timecode in students_timecodes]
        

def group_students(sorted_timecodes: dict = get_sorted_timecodes()):
    pass