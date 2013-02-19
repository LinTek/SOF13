# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Shift.date'
        db.delete_column('functionary_shift', 'date')

        # Adding field 'Shift.start'
        db.add_column('functionary_shift', 'start',
                      self.gf('django.db.models.fields.DateTimeField')(default=None),
                      keep_default=False)

        # Adding field 'Shift.end'
        db.add_column('functionary_shift', 'end',
                      self.gf('django.db.models.fields.DateTimeField')(default=None),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Shift.date'
        raise RuntimeError("Cannot reverse this migration. 'Shift.date' and its values cannot be restored.")
        # Deleting field 'Shift.start'
        db.delete_column('functionary_shift', 'start')

        # Deleting field 'Shift.end'
        db.delete_column('functionary_shift', 'end')


    models = {
        'functionary.functionarytype': {
            'Meta': {'object_name': 'FunctionaryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'functionary.shift': {
            'Meta': {'object_name': 'Shift'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['functionary.FunctionaryType']"}),
            'max_workers': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['functionary']