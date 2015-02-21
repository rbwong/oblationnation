from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from settings import MEDIA_ROOT, MEDIA_URL
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/doc/',
                           include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('social.apps.django_app.urls', namespace='social')),
                       url(r'^', include('customer.urls', namespace='auth')),
                       url(r'^', include('oblation.urls')),
                       )


urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
