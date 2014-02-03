from django.conf.urls import patterns, include, url
from mmm_app.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', landing),
    url(r'^userlogin/$', userlogin),
    url(r'^profile/$', profile),
    url(r'^settings/$', settings),
    url(r'^newproject/$', new_project),
    url(r'^editproject/(?P<proj_id>\w+)/$', edit_project),
    url(r'^project/(?P<proj_id>\w+)/$', view_project),
    url(r'^gallery/$', gallery),
    # url(r'^admin/$', admin),
)
