from django.conf.urls import patterns, url
from .views import IndexView, ShopView, ProductView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^(?P<category>[\w-]+)$',
                           ShopView.as_view(), name='shop'),
                       url(r'^(?P<category>[\w-]+)/(?P<product>[\w-]+)$',
                           ProductView.as_view(), name='product'),
                       )
