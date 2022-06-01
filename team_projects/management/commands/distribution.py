from team_projects.models import AvailableTimecode, Student, Group, Project, Timecode
from django.db.models import Count
import json

PROJECT = Project.objects.all()[0]

def get_sorted_timecodes(project: Project = PROJECT) -> dict:
    timecodes = Project.objects.filter(project=project).
    sorted_timecodes = dict()
    for timecode in timecodes:
        level = timecode.student.level.__str__()
        if level not in sorted_timecodes:
            sorted_timecodes[level] = [{timecode.timecode.converted(): timecode.student}]
        else:
            sorted_timecodes[level].append({timecode.timecode.converted(): timecode.student})
    return sorted_timecodes

def group_students(sorted_timecodes: dict = get_sorted_timecodes()):
    pass