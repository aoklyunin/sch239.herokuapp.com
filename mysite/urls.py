# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import sworks.views


from django.conf import settings
import django.views.static

#import settings
# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^addAttempt/$', sworks.views.addAttempt, name='addAttempt'),
    url(r'^attemptList/$', sworks.views.attemptList, name='attemptList'),
    url(r'^logout/$', sworks.views.logout_view),
    url(r'^register/$', sworks.views.register),
    url(r'^attempt/(?P<attempt_id>[0-9]+)/$', sworks.views.attempt),
    url(r'^personal/$', sworks.views.personal),
    url(r'^addTask/$', sworks.views.addTask),
    url(r'^tasks/$', sworks.views.tasks),
    url(r'^getTasks/$', sworks.views.getTasks),
    url(r'^marks/$', sworks.views.marks),
    url(r'^loadAttempt/(?P<taskName>[а-яА-ЯёЁa-zA-Z0-9_]+)/(?P<taskType>[а-яА-ЯёЁa-zA-Z0-9_]+)/$', sworks.views.loadAttempt),
    url(r'^', sworks.views.index, name='index'),

]
