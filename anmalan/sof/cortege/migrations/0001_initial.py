# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CortegeContribution'
        db.create_table('cortege_cortegecontribution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=40)),
            ('needs_generator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('size_type', self.gf('django.db.models.fields.CharField')(default=1, max_length=10)),
            ('materials', self.gf('django.db.models.fields.TextField')()),
            ('color', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('other', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('idea', self.gf('django.db.models.fields.TextField')()),
            ('participant_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('tickets_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('cortege', ['CortegeContribution'])


    def backwards(self, orm):
        # Deleting model 'CortegeContribution'
        db.delete_table('cortege_cortegecontribution')


    models = {
        'cortege.cortegecontribution': {
            'Meta': {'object_name': 'CortegeContribution'},
            'color': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '40'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.TextField', [], {}),
            'materials': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'needs_generator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'participant_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'size_type': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '10'}),
            'tickets_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['cortege']