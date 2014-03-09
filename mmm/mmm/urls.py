from django.conf.urls import patterns, include, url
from mmm_app.views import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', landing),
    url(r'^login_form/$', user_login_form),
    url(r'^login/$', user_login),
    url(r'^logout/$', user_logout),
    # url(r'^register_form/$', user_register_form),
    url(r'^register/$', user_register),
    url(r'^activate/(?P<username>\w+)/(?P<activation_code>\w+)/$', user_activate),
    url(r'^profile/$', profile_form),
    # url(r'^settings/$', settings),
    # url(r'^newproject/$', new_project),
    # url(r'^editproject/(?P<proj_id>\w+)/$', edit_project),
    # url(r'^project/(?P<proj_id>\w+)/$', view_project),
    # url(r'^gallery/$', gallery),
    # url(r'^admin/$', admin),
    # handles media files
    # url(r'^media/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), 
    # handles static files
    url(r'^static/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), 
)
