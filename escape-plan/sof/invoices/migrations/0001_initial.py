# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Payment'
        db.create_table(u'invoices_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal(u'invoices', ['Payment'])

        # Adding model 'Invoice'
        db.create_table(u'invoices_invoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'invoices', ['Invoice'])

        # Adding M2M table for field tickets on 'Invoice'
        db.create_table(u'invoices_invoice_tickets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('invoice', models.ForeignKey(orm[u'invoices.invoice'], null=False)),
            ('ticket', models.ForeignKey(orm[u'tickets.ticket'], null=False))
        ))
        db.create_unique(u'invoices_invoice_tickets', ['invoice_id', 'ticket_id'])

        # Adding M2M table for field payments on 'Invoice'
        db.create_table(u'invoices_invoice_payments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('invoice', models.ForeignKey(orm[u'invoices.invoice'], null=False)),
            ('payment', models.ForeignKey(orm[u'invoices.payment'], null=False))
        ))
        db.create_unique(u'invoices_invoice_payments', ['invoice_id', 'payment_id'])


    def backwards(self, orm):
        # Deleting model 'Payment'
        db.delete_table(u'invoices_payment')

        # Deleting model 'Invoice'
        db.delete_table(u'invoices_invoice')

        # Removing M2M table for field tickets on 'Invoice'
        db.delete_table('invoices_invoice_tickets')

        # Removing M2M table for field payments on 'Invoice'
        db.delete_table('invoices_invoice_payments')


    models = {
        u'invoices.invoice': {
            'Meta': {'object_name': 'Invoice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payments': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['invoices.Payment']", 'symmetrical': 'False'}),
            'tickets': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tickets.Ticket']", 'symmetrical': 'False'})
        },
        u'invoices.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'tickets.ticket': {
            'Meta': {'object_name': 'Ticket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticket_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tickets.TicketType']"})
        },
        u'tickets.tickettype': {
            'Meta': {'object_name': 'TicketType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        }
    }

    complete_apps = ['invoices']