from team_projects.models import Level, Project, Timecode


PROJECT = Project.objects.all()[0]


def sort_students(project: Project = PROJECT):
    available_timecodes = project.available_timecodes.all()
    students_timecodes = Timecode.objects.filter(project=project).order_by('timecode')
    
    groups = {
        timecode: {'level': None, 'students': []}
        for timecode
        in available_timecodes
    }

    assert isinstance(groups, dict) and len(groups) == len(available_timecodes)

    students = {
        student: [
            timecode.timecode
            for timecode
            in students_timecodes
            if timecode.student == student
        ]
        for student
        in project.students.all()
    }

    for num, timecode in enumerate(available_timecodes):
        if num < 3:
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
            ]
        
        processed_students = list()
        
        for student in suitable_students:
            group_level = groups[timecode]['level']
            student_level = student['student'].level

            if group_level is None and student_level.title != 'middle':
                groups[timecode]['level'] = student_level

            is_compatible = check_level_compatible(group_level, student_level)
            in_group = len(groups[timecode]['students'])

            if is_compatible and in_group < 3:
                groups[timecode]['students'].append((student['student'], student_level.title))
                processed_students.append(student['student'])
        
        for student in processed_students:
            students.pop(student)

    for timecode, info in groups.items():
        print('-' * 20)
        print(timecode)
        print(info['level'])
        print(info['students'])

    print(f'\n{"-" * 20}\nUNSORTED STUDENTS')
    for student in students:
        print(student, student.level.title, students[student])

def check_level_compatible(level1: Level, level2: Level) -> bool:
    try:
        if level1.id > level2.id:
            level1, level2 = level2, level1
        return (level2.id - level1.id) < 2
    except AttributeError:
        return True
