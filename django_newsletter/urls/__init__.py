"""Default urls for the django_newsletter"""
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns

urlpatterns = patterns('',
                       url(r'^mailing/', include('django_newsletter.urls.mailing_list')),
                       url(r'^tracking/', include('django_newsletter.urls.tracking')),
                       url(r'^statistics/', include('django_newsletter.urls.statistics')),
                       url(r'^', include('django_newsletter.urls.newsletter')),
                       )

