# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SpecialInvoice.total_price'
        db.add_column(u'invoices_specialinvoice', 'total_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SpecialInvoice.total_price'
        db.delete_column(u'invoices_specialinvoice', 'total_price')


    models = {
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
        u'invoices.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'denormalized_total_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sent_as_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ocr': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.Person']"}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        u'invoices.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['invoices.Invoice']"})
        },
        u'invoices.specialinvoice': {
            'Meta': {'object_name': 'SpecialInvoice'},
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_handed_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ocr': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['functionary.Person']"}),
            'specification': ('django.db.models.fields.TextField', [], {}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        }
    }

    complete_apps = ['invoices']