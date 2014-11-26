"""Admin for django_newsletter"""
from django.contrib import admin
from django.conf import settings

from django_newsletter.models import Link
from django_newsletter.models import Contact
from django_newsletter.models import WorkGroup
from django_newsletter.models import SMTPServer
from django_newsletter.models import Newsletter
from django_newsletter.models import MailingList
from django_newsletter.models import ContactMailingStatus

from django_newsletter.settings import USE_WORKGROUPS
from django_newsletter.admin.contact import ContactAdmin
from django_newsletter.admin.workgroup import WorkGroupAdmin
from django_newsletter.admin.newsletter import NewsletterAdmin
from django_newsletter.admin.smtpserver import SMTPServerAdmin
from django_newsletter.admin.mailinglist import MailingListAdmin


admin.site.register(Contact, ContactAdmin)
admin.site.register(SMTPServer, SMTPServerAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(MailingList, MailingListAdmin)

if USE_WORKGROUPS:
    admin.site.register(WorkGroup, WorkGroupAdmin)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'creation_date')

if settings.DEBUG:
    admin.site.register(Link, LinkAdmin)
    admin.site.register(ContactMailingStatus)
