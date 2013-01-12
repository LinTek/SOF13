# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('orkester_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('ticket_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('plays_kartege', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('allergies', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('needs_bed', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('attend_sitting', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('t_shirt', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('badge_orchestra', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('badge_visitor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('medal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bottle_opener', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('yoyo', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('orkester', ['Person'])

        # Adding field 'Orchestra.ballet_contact_name'
        db.add_column('orkester_orchestra', 'ballet_contact_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True),
                      keep_default=False)

        # Adding field 'Orchestra.ballet_contact_phone'
        db.add_column('orkester_orchestra', 'ballet_contact_phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True),
                      keep_default=False)

        # Adding field 'Orchestra.ballet_contact_email'
        db.add_column('orkester_orchestra', 'ballet_contact_email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=40, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table('orkester_person')

        # Deleting field 'Orchestra.ballet_contact_name'
        db.delete_column('orkester_orchestra', 'ballet_contact_name')

        # Deleting field 'Orchestra.ballet_contact_phone'
        db.delete_column('orkester_orchestra', 'ballet_contact_phone')

        # Deleting field 'Orchestra.ballet_contact_email'
        db.delete_column('orkester_orchestra', 'ballet_contact_email')


    models = {
        'orkester.orchestra': {
            'Meta': {'object_name': 'Orchestra'},
            'amplifier_bass': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'amplifier_guitar': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'backline': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ballet_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '40', 'blank': 'True'}),
            'ballet_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'ballet_contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'best_memory': ('django.db.models.fields.TextField', [], {}),
            'best_with_sof': ('django.db.models.fields.TextField', [], {}),
            'concerto_grosso': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'concerto_preludium': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'craziest_thing': ('django.db.models.fields.TextField', [], {}),
            'dance': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'departure_day': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'determines_repertory': ('django.db.models.fields.TextField', [], {}),
            'estimated_instruments': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'family_play': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'look_forward_to': ('django.db.models.fields.TextField', [], {}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'microphones': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'mottos': ('django.db.models.fields.TextField', [], {}),
            'music_type': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'orchestra_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'parking_lot_needed': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'parking_lot_type': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'play_friday': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'play_length': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'play_thursday': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'primary_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '40'}),
            'primary_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'primary_contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'rituals': ('django.db.models.fields.TextField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'showpiece': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'sof_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'thing_to_bring': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'three_words': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'uniform_description': ('django.db.models.fields.TextField', [], {}),
            'use_short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'uses_drumset': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'uses_piano': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'vice_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '40'}),
            'vice_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'vice_contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'what_do_you_do': ('django.db.models.fields.TextField', [], {}),
            'why_orchestra': ('django.db.models.fields.TextField', [], {}),
            'will_bring_drumset': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'orkester.person': {
            'Meta': {'object_name': 'Person'},
            'allergies': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'attend_sitting': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'badge_orchestra': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'badge_visitor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bottle_opener': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'medal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'needs_bed': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'plays_kartege': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            't_shirt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'yoyo': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['orkester']