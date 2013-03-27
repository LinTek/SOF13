# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Visitor'
        db.create_table(u'tickets_visitor', (
            (u'person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['functionary.Person'], unique=True, primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'tickets', ['Visitor'])

        # Adding M2M table for field groups on 'Visitor'
        db.create_table(u'tickets_visitor_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visitor', models.ForeignKey(orm[u'tickets.visitor'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'tickets_visitor_groups', ['visitor_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Visitor'
        db.create_table(u'tickets_visitor_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visitor', models.ForeignKey(orm[u'tickets.visitor'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'tickets_visitor_user_permissions', ['visitor_id', 'permission_id'])

        # Adding model 'TicketType'
        db.create_table(u'tickets_tickettype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('opening_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('opening_date_public', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'tickets', ['TicketType'])

        # Adding model 'Ticket'
        db.create_table(u'tickets_ticket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticket_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tickets.TicketType'])),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoices.Invoice'])),
            ('is_handed_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tickets', ['Ticket'])


    def backwards(self, orm):
        # Deleting model 'Visitor'
        db.delete_table(u'tickets_visitor')

        # Removing M2M table for field groups on 'Visitor'
        db.delete_table('tickets_visitor_groups')

        # Removing M2M table for field user_permissions on 'Visitor'
        db.delete_table('tickets_visitor_user_permissions')

        # Deleting model 'TicketType'
        db.delete_table(u'tickets_tickettype')

        # Deleting model 'Ticket'
        db.delete_table(u'tickets_ticket')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'functionary.person': {
            'Meta': {'object_name': 'Person'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lintek_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'invoices.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ocr': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.Person']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'tickets.ticket': {
            'Meta': {'object_name': 'Ticket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['invoices.Invoice']"}),
            'is_handed_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ticket_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tickets.TicketType']"})
        },
        u'tickets.tickettype': {
            'Meta': {'object_name': 'TicketType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'opening_date': ('django.db.models.fields.DateTimeField', [], {}),
            'opening_date_public': ('django.db.models.fields.DateTimeField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        u'tickets.visitor': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Visitor', '_ormbases': [u'functionary.Person']},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['functionary.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['tickets']