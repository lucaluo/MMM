from django.conf.urls import patterns, include, url
from mmm_app.views import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', landing),
    url(r'^login/$', user_login),
    url(r'^logout/$', user_logout),
    url(r'^register/$', user_register),
    url(r'^activate/(?P<username>\w+)/(?P<activation_code>\w+)/$', user_activate),
    url(r'^profile/(?P<prof_id>\w+)/$', profile),
    # url(r'^update_profile/(?P<proj_id>\w+)/$', update_profile),
    # url(r'^settings/$', settings),
    url(r'^new_project/$', new_project),
    # url(r'^update_project/(?P<proj_id>\w+)/$', update_project),
    url(r'^project/(?P<proj_id>\w+)/$', project),
    url(r'^apply_project/$', apply_project),
    url(r'^new_comment/$', new_comment),
    # url(r'^update_comment/(?P<comm_id>\w+)/$', update_comment),
    url(r'^delete_comment/(?P<proj_id>\w+)/(?P<comm_id>\w+)/$', delete_comment),
    # url(r'^gallery/$', gallery),
    url(r'^bookmark/(?P<proj_id>\w+)/$', bookmark),
    url(r'^unbookmark/(?P<proj_id>\w+)/$', unbookmark),
    # handles media files
    url(r'^media/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), 
    # handles static files
    url(r'^static/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), 
)
