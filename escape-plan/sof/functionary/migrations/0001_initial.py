# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FunctionaryType'
        db.create_table('functionary_functionarytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('functionary', ['FunctionaryType'])

        # Adding model 'Shift'
        db.create_table('functionary_shift', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('max_workers', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('job_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['functionary.FunctionaryType'])),
        ))
        db.send_create_signal('functionary', ['Shift'])


    def backwards(self, orm):
        # Deleting model 'FunctionaryType'
        db.delete_table('functionary_functionarytype')

        # Deleting model 'Shift'
        db.delete_table('functionary_shift')


    models = {
        'functionary.functionarytype': {
            'Meta': {'object_name': 'FunctionaryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'functionary.shift': {
            'Meta': {'object_name': 'Shift'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['functionary.FunctionaryType']"}),
            'max_workers': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['functionary']