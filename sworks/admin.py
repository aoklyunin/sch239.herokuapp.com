# -*- coding: utf-8 -*-

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Student,Task,Attempt,AttemptComment,WorkType,TaskType,Mark

# Register your models here.
admin.site.register(Student)
admin.site.register(Task)
admin.site.register(Attempt)
admin.site.register(AttemptComment)
admin.site.register(WorkType)
admin.site.register(TaskType)
admin.site.register(Mark)


UserAdmin.list_display = ('email', 'first_name', 'last_name','is_staff','username')

class AttemptAdmin(admin.ModelAdmin):
    fields = ('student','link')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Attempt, AttemptAdmin)


