# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Member.t_shirt_size'
        db.add_column('orkester_member', 't_shirt_size',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, blank=True),
                      keep_default=False)

        # Adding field 'Member.beer_glass'
        db.add_column('orkester_member', 'beer_glass',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Orchestra.play_length'
        db.delete_column('orkester_orchestra', 'play_length')


    def backwards(self, orm):
        # Deleting field 'Member.t_shirt_size'
        db.delete_column('orkester_member', 't_shirt_size')

        # Deleting field 'Member.beer_glass'
        db.delete_column('orkester_member', 'beer_glass')

        # Adding field 'Orchestra.play_length'
        db.add_column('orkester_orchestra', 'play_length',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, blank=True),
                      keep_default=False)


    models = {
        'orkester.member': {
            'Meta': {'object_name': 'Member'},
            'allergies': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'attend_sitting': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'badge_orchestra': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'badge_visitor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'beer_glass': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bottle_opener': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'medal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'needs_bed': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'orchestras': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['orkester.Orchestra']", 'symmetrical': 'False'}),
            'pid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'plays_kartege': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            't_shirt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            't_shirt_size': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'yoyo': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'orkester.orchestra': {
            'Meta': {'object_name': 'Orchestra'},
            'amplifier_bass': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'amplifier_guitar': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'backline': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ballet_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '40', 'blank': 'True'}),
            'ballet_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'ballet_contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'ballet_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'best_memory': ('django.db.models.fields.TextField', [], {}),
            'best_with_sof': ('django.db.models.fields.TextField', [], {}),
            'concerto_grosso': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'concerto_preludium': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'craziest_thing': ('django.db.models.fields.TextField', [], {}),
            'dance': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'departure_day': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'determines_repertory': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'estimated_instruments': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'family_play': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'look_forward_to': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'microphones': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mottos': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'music_type': ('django.db.models.fields.TextField', [], {}),
            'orchestra_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'orchestra_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parking_lot_needed': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'parking_lot_type': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'play_friday': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'play_thursday': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'primary_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '40'}),
            'primary_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'primary_contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'rituals': ('django.db.models.fields.TextField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'showpiece': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'sof_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'thing_to_bring': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'three_words': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'uniform_description': ('django.db.models.fields.TextField', [], {}),
            'use_short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'uses_drumset': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'uses_piano': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'vice_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '40'}),
            'vice_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'vice_contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'what_do_you_do': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'why_orchestra': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'will_bring_drumset': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['orkester']