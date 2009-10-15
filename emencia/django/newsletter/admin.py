"""Admin for emencia.django.newsletter"""
from datetime import datetime
from django.contrib import admin
from django.utils.translation import ugettext as _

from emencia.django.newsletter.models import SMTPServer
from emencia.django.newsletter.models import Contact
from emencia.django.newsletter.models import MailingList
from emencia.django.newsletter.models import Newsletter
from emencia.django.newsletter.models import ContactMailingStatus

class SMTPServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'port', 'user', 'tls', 'mails_hour')
    list_filter = ('tls',)
    search_fields = ('name', 'host', 'user',)
    fieldsets = ((None, {'fields': ('name',),}),
                 (_('Configuration'), {'fields': ('host', 'port',
                                                  'user', 'password', 'tls'),}),
                 (_('Miscellaneous'), {'fields': ('mails_hour',),}),
                 )
    actions_on_top = False
    actions_on_bottom = False
    
admin.site.register(SMTPServer, SMTPServerAdmin)

class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('email', 'first_name', 'last_name', 'subscriber',
                    'invalid', 'tags', 'creation_date')
    list_filter = ('subscriber', 'invalid', 'creation_date', 'modification_date')
    search_fields = ('email', 'first_name', 'last_name', 'tags')
    fieldsets = ((None, {'fields': ('email', 'first_name', 'last_name')}),
                 (None, {'fields': ('tags',)}),
                 (_('Status'), {'fields': ('subscriber', 'invalid')}),
                 (_('Advanced'), {'fields': ('object_id', 'content_type'),
                                  'classes': ('collapse',)}),
                 )
    actions_on_top = False
    actions_on_bottom = False

admin.site.register(Contact, ContactAdmin)

class MailingListAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('name', 'description', 'contacts_length',
                    'creation_date', 'modification_date')    
    list_filter = ('creation_date', 'modification_date')
    search_fields = ('name', 'description',)
    filter_horizontal = ['contacts']
    fieldsets = ((None, {'fields': ('name', 'description',)}),
                 (None, {'fields': ('contacts',)}),
                 )
    actions = ['merge_mailinglist',]
    actions_on_top = False
    actions_on_bottom = True

    def merge_mailinglist(self, request, queryset):
        if queryset.count() == 1:
            self.message_user(request, _('Please select a least 2 mailing list.'))
            return None
        
        contacts = {}
        for ml in queryset:
            for contact in ml.contacts.all():
                contacts[contact] = ''

        when = str(datetime.now()).split('.')[0]
        new_mailing = MailingList(name=_('Merging list at %s') % when, 
                                  description=_('Mailing list created by merging at %s') % when)
        new_mailing.save()
        new_mailing.contacts = contacts.keys()
        
        self.message_user(request, _('%s succesfully created by merging.') % new_mailing)
        
    merge_mailinglist.short_description = _('Merge selected mailinglists')
    

admin.site.register(MailingList, MailingListAdmin)


class NewsletterAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('title', 'mailing_list', 'server', 'status',
                    'sending_date', 'creation_date', 'modification_date')
    list_filter = ('mailing_list', 'server', 'status', 'sending_date',
                   'creation_date', 'modification_date')
    search_fields = ('title', 'content', 'header_sender', 'header_reply')
    filter_horizontal = ['test_contacts']
    fieldsets = ((None, {'fields': ('title', 'content',)}),
                 (_('Receivers'), {'fields': ('mailing_list', 'test_contacts',)}),
                 (_('Sending'), {'fields': ('sending_date', 'status',)}),
                 (_('Miscellaneous'), {'fields': ('server', 'header_sender',
                                                  'header_reply'),
                                       'classes': ('collapse',)}),                 
                 )

    actions_on_top = False
    actions_on_bottom = False

admin.site.register(Newsletter, NewsletterAdmin)

#admin.site.register(ContactMailingStatus)
