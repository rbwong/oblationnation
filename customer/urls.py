from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from .views import logoutnow, ProfileView


urlpatterns = patterns('',
                       url(r'^logout/$', logoutnow, name='logout'),
                       url(r'^profile/$', login_required(ProfileView.as_view()), name='userprofile'),
                       )
