# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Worker.phone_number'
        db.add_column(u'functionary_worker', 'phone_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Worker.tshirt_size'
        db.add_column(u'functionary_worker', 'tshirt_size',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=4, blank=True),
                      keep_default=False)

        # Adding field 'Worker.ice_number'
        db.add_column(u'functionary_worker', 'ice_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Worker.allergies'
        db.add_column(u'functionary_worker', 'allergies',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Worker.other'
        db.add_column(u'functionary_worker', 'other',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Worker.phone_number'
        db.delete_column(u'functionary_worker', 'phone_number')

        # Deleting field 'Worker.tshirt_size'
        db.delete_column(u'functionary_worker', 'tshirt_size')

        # Deleting field 'Worker.ice_number'
        db.delete_column(u'functionary_worker', 'ice_number')

        # Deleting field 'Worker.allergies'
        db.delete_column(u'functionary_worker', 'allergies')

        # Deleting field 'Worker.other'
        db.delete_column(u'functionary_worker', 'other')


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
        u'functionary.person': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Person'},
            'barcode_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'lintek_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'liu_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'rfid_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'functionary.shift': {
            'Meta': {'object_name': 'Shift'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_dummy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_workers': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'responsible_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'shift_sub_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.ShiftSubType']", 'null': 'True', 'blank': 'True'}),
            'shift_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.ShiftType']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'functionary.shiftsubtype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ShiftSubType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'functionary.shifttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ShiftType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'functionary.visitor': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Visitor', '_ormbases': [u'functionary.Person']},
            u'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['functionary.Person']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'functionary.worker': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Worker', '_ormbases': [u'functionary.Person']},
            'allergies': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'contract_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ice_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'orchestra_worker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['functionary.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'super_worker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tshirt_size': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'welcome_email_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'functionary.workerregistration': {
            'Meta': {'object_name': 'WorkerRegistration'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.Shift']"}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.Worker']"})
        }
    }

    complete_apps = ['functionary']