from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import IndexView, ShopView, ProductView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^(?P<category>[\w-]+)$/',
                           ShopView.as_view(), name='shop'),
                       url(r'^(?P<category>[\w-]+)/(?P<product>[\w-]+)/$',
                           ProductView.as_view(), name='product'),
                       url(r'^about/', TemplateView.as_view(template_name="about.html"), name='about'),
                       url(r'^faqs/', TemplateView.as_view(template_name="faqs.html"), name='faqs'),
                       url(r'^termsconditions/', TemplateView.as_view(template_name="termsconditions.html"), name='terms'),
                       url(r'^thanks/', TemplateView.as_view(template_name="thankyou.html"), name='thankyou'),
                       )
