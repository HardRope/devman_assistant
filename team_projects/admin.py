from django.contrib import admin

from .models import Project, Mentor, Student, Timecode, Level, Group


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'level')
    raw_id_fields = ("projects", 'groups')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'start_date', 'finish_date', 'is_active')
    raw_id_fields = ("students", 'timecodes')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('number', 'project')


@admin.register(Timecode)
class TimecodeAdmin(admin.ModelAdmin):
    list_display = ('time',)
