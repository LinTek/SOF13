# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Orchestra'
        db.create_table('orkester_orchestra', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('use_short_name', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('sof_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('look_forward_to', self.gf('django.db.models.fields.TextField')()),
            ('music_type', self.gf('django.db.models.fields.TextField')()),
            ('best_memory', self.gf('django.db.models.fields.TextField')()),
            ('rituals', self.gf('django.db.models.fields.TextField')()),
            ('three_words', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('showpiece', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('best_with_sof', self.gf('django.db.models.fields.TextField')()),
            ('why_orchestra', self.gf('django.db.models.fields.TextField')()),
            ('craziest_thing', self.gf('django.db.models.fields.TextField')()),
            ('determines_repertory', self.gf('django.db.models.fields.TextField')()),
            ('what_do_you_do', self.gf('django.db.models.fields.TextField')()),
            ('uniform_description', self.gf('django.db.models.fields.TextField')()),
            ('dance', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('thing_to_bring', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('mottos', self.gf('django.db.models.fields.TextField')()),
            ('orchestra_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('logo_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('departure_day', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('parking_lot_needed', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('parking_lot_type', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('estimated_instruments', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('play_thursday', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('play_friday', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('play_length', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('concerto_preludium', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('concerto_grosso', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('family_play', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('backline', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('amplifier_guitar', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('amplifier_bass', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('uses_drumset', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('will_bring_drumset', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('uses_piano', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('microphones', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('primary_contact_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('primary_contact_phone', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('primary_contact_email', self.gf('django.db.models.fields.EmailField')(max_length=40)),
            ('vice_contact_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('vice_contact_phone', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('vice_contact_email', self.gf('django.db.models.fields.EmailField')(max_length=40)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('orkester', ['Orchestra'])


    def backwards(self, orm):
        # Deleting model 'Orchestra'
        db.delete_table('orkester_orchestra')


    models = {
        'orkester.orchestra': {
            'Meta': {'object_name': 'Orchestra'},
            'amplifier_bass': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'amplifier_guitar': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'backline': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
        }
    }

    complete_apps = ['orkester']