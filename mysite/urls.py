# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin
import sworks.auth
import sworks.views

# автоопределение администратора
admin.autodiscover()

urlpatterns = [
    # панель администратора
    url(r'^admin/', include(admin.site.urls)),
    # добавить попытку
    url(r'^addAttempt/$', sworks.views.addAttempt, name='addAttempt'),
    # список попыток
    url(r'^attemptList/$', sworks.views.attemptList, name='attemptList'),
    # список принятых попыток
    url(r'^successAttemptList/$', sworks.views.successAttemptList, name='successAttemptList'),
    # выход из сайта
    url(r'^logout/$', sworks.auth.logout_view),
    # регистрация на сайте
    url(r'^register/$', sworks.auth.register),
    # просмотр попытки
    url(r'^attempt/(?P<attempt_id>[0-9]+)/$', sworks.views.attempt),
    # принять попытку
    url(r'^attempt/success/(?P<attempt_id>[0-9]+)/$', sworks.views.success),
    # отклонить попытку
    url(r'^attempt/drop/(?P<attempt_id>[0-9]+)/$', sworks.views.drop),
    # личный кабинет
    url(r'^personal/$', sworks.views.personal),
    # добавить задание
    url(r'^addTask/$', sworks.views.addTask),
    # получить задание
    url(r'^getTasks/$', sworks.views.getTasks),
    # журнал
    url(r'^marks/$', sworks.views.marks),
    url(r'^cheaters/punish/(?P<p_id>[0-9]+)/$', sworks.views.punishCheater),
    url(r'^cheaters/drop/(?P<p_id>[0-9]+)/$', sworks.views.dropCheater),
    url(r'^cheaters/$', sworks.views.cheaters),
    # просмотр конкретного задания
    url(r'^markView/(?P<mark_id>[0-9]+)/$', sworks.views.markView),
    # на главную страницу
    url(r'^punished/$', sworks.views.punished),
    url(r'^', sworks.auth.index, name='index'),
#cheaters/punish/{{p.id}}/">Списывали</a>
 #           <a href="../../../cheaters/drop/{{p.id}}

]
