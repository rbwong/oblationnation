from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from shop import urls as shop_urls
from .settings import local
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'django_project.views.home', name='home'),
                       url(r'^shop/', include(shop_urls)),
                       url(r'^', include('order.urls')),
                       url(r'^', include('oblation.urls')),
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/doc/',
                           include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )


urlpatterns += static(local.MEDIA_URL, document_root=local.MEDIA_ROOT)
urlpatterns += static(local.STATIC_URL, document_root=local.STATIC_ROOT)
