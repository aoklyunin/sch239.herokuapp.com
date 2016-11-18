# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Student,Task,Attempt,AttemptComment

# Register your models here.
admin.site.register(Student)
admin.site.register(Task)
admin.site.register(Attempt)
admin.site.register(AttemptComment)