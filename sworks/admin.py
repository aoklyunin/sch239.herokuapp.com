# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Student, Task, Attempt, AttemptComment, WorkType, TaskType, Mark, CodeLanguage, ProgramCode, PretendToCheat, \
    PretendVal

admin.site.register(Student)
admin.site.register(Task)
admin.site.register(AttemptComment)
admin.site.register(WorkType)
admin.site.register(TaskType)
admin.site.register(CodeLanguage)
admin.site.register(ProgramCode)
admin.site.register(PretendToCheat)
admin.site.register(PretendVal)



# если нужно сделать своё представление модели в админке, нужно убрать её регистрацию из списка выше

UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_staff', 'username')


class AttemptAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'link')


class MarkAdmin(admin.ModelAdmin):
    list_display = ('task', 'link', 'm_value')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Mark, MarkAdmin)
