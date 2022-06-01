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
    description = models.TextField('Описание проекта')
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
        related_name='projects'
    )
    
    timecodes = models.ManyToManyField(
        'Timecode',
        verbose_name='Таймкоды созвона',
        related_name='projects',
    )
    is_active = models.BooleanField('Проект в процессе', default=True)

    def __str__(self):
        return f'{self.title} ({self.start_date} - {self.finish_date})'


class Group(models.Model):
    number = models.SmallIntegerField('Номер группы')
    project = models.ForeignKey(
        'Project',
        verbose_name='Проект',
        related_name='groups',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.number} группа'


class Timecode(models.Model):
    time = models.TimeField('Время созвона')

    def __str__(self):
        return f'{self.time}'
