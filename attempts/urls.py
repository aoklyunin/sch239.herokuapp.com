# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.attempt, name='index'),
    url(r'^attemptList$', views.attemptList, name='attemotList'),
    url(r'^/remove/(?P<attemptId>[0-9]+)$', views.removeAttempt, name='remove')
]
