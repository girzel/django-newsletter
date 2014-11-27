# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django_newsletter.models
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file_attachment', models.FileField(upload_to=django_newsletter.models.get_newsletter_storage_path, max_length=255, verbose_name='file to attach')),
            ],
            options={
                'db_table': 'newsletter_attachment',
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=150, verbose_name='email')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=150, verbose_name='last name', blank=True)),
                ('subscriber', models.BooleanField(default=True, verbose_name='subscriber')),
                ('valid', models.BooleanField(default=True, verbose_name='valid email')),
                ('tester', models.BooleanField(default=False, verbose_name='contact tester')),
                ('tags', tagging.fields.TagField(max_length=255, verbose_name='tags', blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='modification date')),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('creation_date',),
                'db_table': 'newsletter_contact',
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactMailingStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(verbose_name='status', choices=[(-1, 'sent in test'), (0, 'sent'), (1, 'error'), (2, 'invalid email'), (4, 'opened'), (5, 'opened on site'), (6, 'link opened'), (7, 'unsubscription')])),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('contact', models.ForeignKey(verbose_name='contact', to='django_newsletter.Contact')),
            ],
            options={
                'ordering': ('-creation_date',),
                'db_table': 'newsletter_contactmailingstatus',
                'verbose_name': 'contact mailing status',
                'verbose_name_plural': 'contact mailing statuses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('url', models.CharField(max_length=255, verbose_name='url')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
            ],
            options={
                'ordering': ('-creation_date',),
                'db_table': 'newsletter_link',
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='modification date')),
                ('subscribers', models.ManyToManyField(related_name='mailinglist_subscriber', verbose_name='subscribers', to='django_newsletter.Contact')),
                ('unsubscribers', models.ManyToManyField(related_name='mailinglist_unsubscriber', null=True, verbose_name='unsubscribers', to='django_newsletter.Contact', blank=True)),
            ],
            options={
                'ordering': ('-creation_date',),
                'db_table': 'newsletter_mailinglist',
                'verbose_name': 'mailing list',
                'verbose_name_plural': 'mailing lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='You can use the "{{ UNIQUE_KEY }}" variable for unique identifier within the newsletter\'s title.', max_length=255, verbose_name='title')),
                ('content', models.TextField(default='<body>\n<!-- Edit your newsletter here -->\n</body>', help_text='Or paste an URL.', verbose_name='content')),
                ('header_sender', models.CharField(default=b'Paper Republic Newsletter <news@paper-republic.org>', max_length=255, verbose_name='sender')),
                ('header_reply', models.CharField(default=b'Paper Republic Newsletter <news@paper-republic.org>', max_length=255, verbose_name='reply to')),
                ('status', models.IntegerField(default=0, verbose_name='status', choices=[(0, 'draft'), (1, 'waiting sending'), (2, 'sending'), (4, 'sent'), (5, 'canceled')])),
                ('sending_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='sending date')),
                ('slug', models.SlugField(help_text='Used for displaying the newsletter on the site.', unique=True, max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='modification date')),
                ('mailing_list', models.ForeignKey(verbose_name='mailing list', to='django_newsletter.MailingList')),
            ],
            options={
                'ordering': ('-creation_date',),
                'db_table': 'newsletter_newsletter',
                'verbose_name': 'newsletter',
                'verbose_name_plural': 'newsletters',
                'permissions': (('can_change_status', 'Can change status'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SMTPServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('host', models.CharField(max_length=255, verbose_name='server host')),
                ('user', models.CharField(help_text='Leave empty if the host is public.', max_length=128, verbose_name='server user', blank=True)),
                ('password', models.CharField(help_text='Leave empty if the host is public.', max_length=128, verbose_name='server password', blank=True)),
                ('port', models.IntegerField(default=25, verbose_name='server port')),
                ('tls', models.BooleanField(default=False, verbose_name='server use TLS')),
                ('headers', models.TextField(help_text='key1: value1 key2: value2, splitted by return line.\nUseful for passing some tracking headers if your provider allows it.', verbose_name='custom headers', blank=True)),
                ('mails_hour', models.IntegerField(default=0, help_text='E-Mail sending rate in messages per hour', verbose_name='e-mail send rate')),
                ('emails_remains', models.IntegerField(default=10000, help_text='Sendable E-Mail in the current account', verbose_name='remaining e-mail')),
            ],
            options={
                'db_table': 'newsletter_smtpserver',
                'verbose_name': 'SMTP server',
                'verbose_name_plural': 'SMTP servers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('contacts', models.ManyToManyField(to='django_newsletter.Contact', null=True, verbose_name='contacts', blank=True)),
                ('group', models.ForeignKey(verbose_name='permissions group', to='auth.Group')),
                ('mailinglists', models.ManyToManyField(to='django_newsletter.MailingList', null=True, verbose_name='mailing lists', blank=True)),
                ('newsletters', models.ManyToManyField(to='django_newsletter.Newsletter', null=True, verbose_name='newsletters', blank=True)),
            ],
            options={
                'db_table': 'newsletter_workgroup',
                'verbose_name': 'workgroup',
                'verbose_name_plural': 'workgroups',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='server',
            field=models.ForeignKey(default=1, verbose_name='smtp server', to='django_newsletter.SMTPServer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newsletter',
            name='test_contacts',
            field=models.ManyToManyField(to='django_newsletter.Contact', null=True, verbose_name='test contacts', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactmailingstatus',
            name='link',
            field=models.ForeignKey(verbose_name='link', blank=True, to='django_newsletter.Link', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactmailingstatus',
            name='newsletter',
            field=models.ForeignKey(verbose_name='newsletter', to='django_newsletter.Newsletter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='newsletter',
            field=models.ForeignKey(verbose_name='newsletter', to='django_newsletter.Newsletter'),
            preserve_default=True,
        ),
    ]
