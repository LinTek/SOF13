# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FunctionaryType'
        db.delete_table(u'functionary_functionarytype')

        # Adding model 'ShiftType'
        db.create_table(u'functionary_shifttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'functionary', ['ShiftType'])

        # Adding model 'Functionary'
        db.create_table(u'functionary_functionary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('liu_id', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('liu_card_no', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'functionary', ['Functionary'])

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


        # Changing field 'Shift.job_type'
        db.alter_column(u'functionary_shift', 'job_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['functionary.ShiftType']))

    def backwards(self, orm):
        # Adding model 'FunctionaryType'
        db.create_table(u'functionary_functionarytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('functionary', ['FunctionaryType'])

        # Deleting model 'ShiftType'
        db.delete_table(u'functionary_shifttype')

        # Deleting model 'Functionary'
        db.delete_table(u'functionary_functionary')

        # Removing M2M table for field groups on 'Functionary'
        db.delete_table('functionary_functionary_groups')

        # Removing M2M table for field user_permissions on 'Functionary'
        db.delete_table('functionary_functionary_user_permissions')


        # Changing field 'Shift.job_type'
        db.alter_column(u'functionary_shift', 'job_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['functionary.FunctionaryType']))

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
        u'functionary.functionary': {
            'Meta': {'object_name': 'Functionary'},
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
            'liu_card_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'liu_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'functionary.shift': {
            'Meta': {'object_name': 'Shift'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.ShiftType']"}),
            'max_workers': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'functionary.shifttype': {
            'Meta': {'object_name': 'ShiftType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['functionary']