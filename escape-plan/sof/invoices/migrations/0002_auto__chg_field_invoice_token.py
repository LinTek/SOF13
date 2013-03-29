# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Invoice.token'
        db.alter_column(u'invoices_invoice', 'token', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'Invoice.token'
        db.alter_column(u'invoices_invoice', 'token', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
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
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'invoices.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['invoices.Invoice']"})
        }
    }

    complete_apps = ['invoices']