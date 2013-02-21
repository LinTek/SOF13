# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Functionary.username'
        db.delete_column(u'functionary_functionary', 'username')

        # Deleting field 'Functionary.first_name'
        db.delete_column(u'functionary_functionary', 'first_name')

        # Deleting field 'Functionary.last_name'
        db.delete_column(u'functionary_functionary', 'last_name')

        # Deleting field 'Functionary.is_staff'
        db.delete_column(u'functionary_functionary', 'is_staff')

        # Deleting field 'Functionary.is_active'
        db.delete_column(u'functionary_functionary', 'is_active')

        # Deleting field 'Functionary.is_superuser'
        db.delete_column(u'functionary_functionary', 'is_superuser')

        # Deleting field 'Functionary.email'
        db.delete_column(u'functionary_functionary', 'email')

        # Deleting field 'Functionary.date_joined'
        db.delete_column(u'functionary_functionary', 'date_joined')

        # Removing M2M table for field groups on 'Functionary'
        db.delete_table('functionary_functionary_groups')

        # Removing M2M table for field user_permissions on 'Functionary'
        db.delete_table('functionary_functionary_user_permissions')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Functionary.username'
        raise RuntimeError("Cannot reverse this migration. 'Functionary.username' and its values cannot be restored.")
        # Adding field 'Functionary.first_name'
        db.add_column(u'functionary_functionary', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'Functionary.last_name'
        db.add_column(u'functionary_functionary', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'Functionary.is_staff'
        db.add_column(u'functionary_functionary', 'is_staff',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Functionary.is_active'
        db.add_column(u'functionary_functionary', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Functionary.is_superuser'
        db.add_column(u'functionary_functionary', 'is_superuser',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Functionary.email'
        db.add_column(u'functionary_functionary', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True),
                      keep_default=False)

        # Adding field 'Functionary.date_joined'
        db.add_column(u'functionary_functionary', 'date_joined',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding M2M table for field groups on 'Functionary'
        db.create_table(u'functionary_functionary_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('functionary', models.ForeignKey(orm[u'functionary.functionary'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'functionary_functionary_groups', ['functionary_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Functionary'
        db.create_table(u'functionary_functionary_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('functionary', models.ForeignKey(orm[u'functionary.functionary'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'functionary_functionary_user_permissions', ['functionary_id', 'permission_id'])


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'functionary.functionary': {
            'Meta': {'object_name': 'Functionary'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'liu_card_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'liu_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'functionary.shift': {
            'Meta': {'object_name': 'Shift'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_workers': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'responsible_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'shift_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.ShiftType']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'functionary.shifttype': {
            'Meta': {'object_name': 'ShiftType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'functionary.workerregistration': {
            'Meta': {'object_name': 'WorkerRegistration'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.Shift']"}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['functionary']