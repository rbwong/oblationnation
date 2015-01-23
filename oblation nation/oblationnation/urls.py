from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    url(r'^', include('shop.urls')),
    url(r'^', include('order.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
