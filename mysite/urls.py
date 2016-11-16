from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import sworks.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^attempt', include('sworks.urls')),
    url(r'^addAttempt$', sworks.views.addAttempt, name='addAttempt'),
    url(r'^attemptList', sworks.views.attemptList, name='attemptList'),
    url(r'^', sworks.views.index, name='index'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }
 )
    
]
