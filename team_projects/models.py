import uuid

from django.core.validators import MinLengthValidator
from django.db import models


class Mentor(models.Model):
    last_name = models.CharField('Фамилия', max_length=20)
    first_name = models.CharField('Имя', max_length=20)
    patronymic = models.CharField('Отчество', max_length=20, blank=True)
    telegram_id = models.SmallIntegerField('Telegram_id')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    last_name = models.CharField('Фамилия', max_length=20)
    first_name = models.CharField('Имя', max_length=20)
    patronymic = models.CharField('Отчество', max_length=20, blank=True)
    telegram_id = models.SmallIntegerField('Telegram_id')
    level = models.ForeignKey(
        'Level',
        verbose_name='Уровень подготовки',
        related_name='students',
        on_delete=models.PROTECT,
    )
    groups = models.ManyToManyField(
        'Group',
        verbose_name='Учебные группы',
        related_name='students',
        blank=True
    )
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Level(models.Model):
    title = models.CharField("Уровень", max_length=20)

    def __str__(self):
        return self.title


class Project(models.Model):
    uuid = models.CharField(
        "id",
        unique=True,
        default=uuid.uuid1,
        max_length=36,
        validators=[MinLengthValidator(36)],
        primary_key=True,
        editable=False
    )
    title = models.CharField('Название проекта', max_length=50)
    description = models.TextField('Описание проекта', blank=True)
    briefing = models.URLField('Ссылка на бриф')
    mentor = models.ForeignKey(
        'Mentor',
        verbose_name='Ментор',
        related_name='projects',
        on_delete=models.PROTECT
    )
    start_date = models.DateField('Дата начала проекта')
    finish_date = models.DateField('Дата окончания проекта')
    students = models.ManyToManyField(
        'Student',
        verbose_name='Участники',
        related_name='projects',
    )
    
    available_timecodes = models.ManyToManyField(
        'AvailableTimecode',
        verbose_name='Таймкоды созвона',
        related_name='projects',
    )

    groups_formed = models.BooleanField('Группы сформированы', default=False)

    is_active = models.BooleanField('Проект в процессе', default=True)

    def __str__(self):
        return f'{self.title} ({self.start_date} - {self.finish_date})'


class Group(models.Model):
    number = models.SmallIntegerField('Номер группы')
    timecode = models.ForeignKey(
        'AvailableTimecode',
        verbose_name='Время созвона',
        related_name='groups',
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        'Project',
        verbose_name='Проект',
        related_name='groups',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.number} группа'


class AvailableTimecode(models.Model):
    time = models.TimeField('Время созвона')

    def __str__(self):
        return f'{self.time}'

    def converted(self):
        return self.time.hour * 60 + self.time.minute


class Timecode(models.Model):
    timecode = models.ForeignKey(
        'AvailableTimecode',
        verbose_name='Время созвона',
        related_name='project_timecodes',
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        'Project',
        verbose_name='Проект',
        related_name='timecodes',
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        'Student',
        verbose_name='Студент',
        related_name='timecodes',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.project}: {self.student} - {self.timecode}'
