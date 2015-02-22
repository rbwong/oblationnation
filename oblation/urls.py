from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import IndexView, ShopView, ProductView, AboutView, FAQsView, TermsConditionsView, ThankYouView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^about/$', AboutView.as_view(), name='about'),
                       url(r'^faqs/$', FAQsView.as_view(), name='faqs'),
                       url(r'^termsconditions/$',
                           TermsConditionsView.as_view(), name='terms'),
                       url(r'^thanks/$', ThankYouView.as_view(), name='thankyou'),
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^(?P<category>[\w-]+)/$',
                           ShopView.as_view(), name='shop'),
                       url(r'^(?P<category>[\w-]+)/(?P<product>[\w-]+)/$',
                           ProductView.as_view(), name='product'),
                       )
