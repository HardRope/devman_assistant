import random

from django.db import migrations

def add_timecodes(apps, schema_editor):
    Mentor = apps.get_model('team_projects', 'Mentor')
    Student = apps.get_model('team_projects', 'Student')
    Level = apps.get_model('team_projects', 'Level')
    Project = apps.get_model('team_projects', 'Project')
    AvailableTimecode = apps.get_model('team_projects', 'AvailableTimecode')
    Timecode = apps.get_model('team_projects', 'Timecode')
    
    project = Project.objects.get(title='DVMN TEST')
    students = project.students.all()
    available_timecodes = project.available_timecodes.all()
    for _ in range(len(students)):
        timecode, _ = Timecode.objects.get_or_create(
            timecode=random.choice(available_timecodes),
            project=project,
            student=students[_],
        )
        timecode.save()
        timecode, _ = Timecode.objects.get_or_create(
            timecode=random.choice(available_timecodes),
            project=project,
            student=students[_],
        )
        timecode.save()
        timecode, _ = Timecode.objects.get_or_create(
            timecode=random.choice(available_timecodes),
            project=project,
            student=students[_],
        )
        timecode.save()

class Migration(migrations.Migration):

    dependencies = [
        ('team_projects', '0002_input_default_values'),
    ]

    operations = [
        migrations.RunPython(add_timecodes)
    ]
