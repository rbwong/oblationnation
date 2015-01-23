from django.conf.urls import patterns, include, url
from .views import IndexView
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='home_page'),
                       )
