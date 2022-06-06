from datetime import time
from textwrap import dedent
from django.db.models.query import QuerySet
from team_projects.management.commands.distribution import sort_students
from team_projects.models import AvailableTimecode, Group, Mentor, Project, Student, Timecode


class GroupCorrectionError(Exception):
    def __str__(self, project: Project):
        return dedent(
            f'''Группы в проекте 
            "{project}" 
            уже сформированы.
            
            Дальнейшие корректировки невозможны.'''
        )


class ProjectFinishedError(Exception):
    def __str__(self, project: Project):
        return dedent(
            f'''"{project}" 
            завершен.
            
            Дальнейшие корректировки невозможны.'''
        )


def get_actual_projects() -> Project:
    return Project.objects.filter(is_active=True)


def get_project(uuid: str) -> Project:
    return Project.objects.get(uuid=uuid)


def get_participants(project: Project) -> QuerySet(Student):
    return project.students.all()


def get_student(telegram_id: int) -> Student:
    return Student.objects.get(telegram_id=telegram_id)


def get_mentors() -> QuerySet:
    return Mentor.objects.all()


def get_students(project: Project = None) -> QuerySet:
    if project:
        return project.students.all()
    else:
        return Student.objects.all()


def groups_formed_set(project: Project) -> bool:
    project.groups_formed = True
    project.save()
    return project.groups_formed


def get_timecodes_buttons(student: Student,
                          project: Project) -> dict():
    if not project.is_active:
        raise ProjectFinishedError(project)
    elif project.groups_formed:
        raise GroupCorrectionError(project)
    project_timecodes = project.available_timecodes.all()
    project_datetimes = [timecode.time for timecode in project_timecodes]
    student_timecodes = Timecode.objects.filter(
        project=project,
        student=student
    )
    available_timecodes = list()
    for timecode in project_timecodes:
        interval_time = time(hour=timecode.time.hour + 1, minute=timecode.time.minute)
        if (timecode in student_timecodes 
            or interval_time not in project_datetimes):
            continue
        available_timecodes.append(f'{timecode.time} - {interval_time}')
    if not available_timecodes:
        available_timecodes = None
    return {student: available_timecodes}


def get_project_groups(project: Project) -> dict():
    groups = dict()
    for group in Group.objects.filter(project=project):
        groups[group] = group.students.all()
    return groups


def get_current_student_group(student: Student, project: Project) -> Group:
    return student.groups.get(project=project)


def save_timecode(convenient_time: time,
                  student: Student,
                  project: Project) -> Timecode:
    if not project.is_active:
        raise ProjectFinishedError(project)
    elif project.groups_formed:
        raise GroupCorrectionError(project)

    available_timecode = AvailableTimecode.objects.get(time=convenient_time)
    timecode, _ = Timecode.objects.get_or_create(
        timecode=available_timecode,
        project=project,
        student=student
    )
    return timecode


def get_current_timecodes(student: Student,
                          project: Project) -> QuerySet(Timecode):
    if not project.is_active:
        raise ProjectFinishedError(project)
    return project.timecodes.filter(student=student)


def delete_timecode(timecode: Timecode) -> tuple():
    if not timecode.project.is_active:
        raise ProjectFinishedError(timecode.project)
    elif timecode.project.groups_formed:
        raise GroupCorrectionError(timecode.project)
    return timecode.delete()


def confirm_groups(project: Project):
    groups, students = sort_students(project)
    for timecode, group in groups.items():
        group_object, _ = Group.objects.get_or_create(
            timecode=timecode,
            project=project
        )
        for student in group['students']:
            student.groups.add(group_object)
            student.save
    available_timecodes = project.available_timecodes.all()
    return len(get_project_groups(project)) == len(available_timecodes)
    