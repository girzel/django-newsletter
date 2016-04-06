"""Urls for the django_newsletter Mailing List"""
from django.conf.urls import url
from django_newsletter.views import mailing_list

from django_newsletter.forms import MailingListSubscriptionForm
from django_newsletter.forms import AllMailingListSubscriptionForm

urlpatterns = [
    url(r'^unsubscribe/(?P<slug>[-\w]+)/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        mailing_list.view_mailinglist_unsubscribe,
        name='newsletter_mailinglist_unsubscribe'),
    url(r'^subscribe/(?P<mailing_list_id>\d+)/',
        mailing_list.view_mailinglist_subscribe,
        {'form_class': MailingListSubscriptionForm},
        name='newsletter_mailinglist_subscribe'),
    url(r'^subscribe/',
        mailing_list.view_mailinglist_subscribe,
        {'form_class': AllMailingListSubscriptionForm},
        name='newsletter_mailinglist_subscribe_all'),]
