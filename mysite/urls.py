# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import sworks.views
import sworks.auth

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
    url(r'^logout/$', sworks.auth.logout_view),
    url(r'^register/$', sworks.auth.register),
    url(r'^attempt/(?P<attempt_id>[0-9]+)/$', sworks.views.attempt),
    url(r'^attempt/success/(?P<attempt_id>[0-9]+)/$', sworks.views.success),
    url(r'^attempt/drop/(?P<attempt_id>[0-9]+)/$', sworks.views.drop),
    url(r'^personal/$', sworks.views.personal),
    url(r'^addTask/$', sworks.views.addTask),
    url(r'^getTasks/$', sworks.views.getTasks),
    url(r'^marks/$', sworks.views.marks),
    url(r'^markView/(?P<mark_id>[0-9]+)/$', sworks.views.markView),
    url(u'^loadAttempt/(?P<taskName>[а-яА-ЯёЁa-zA-Z0-9_]+)/(?P<taskType>[а-яА-ЯёЁa-zA-Z0-9_]+)/$', sworks.views.loadAttempt),
    url(r'^', sworks.auth.index, name='index'),

]
