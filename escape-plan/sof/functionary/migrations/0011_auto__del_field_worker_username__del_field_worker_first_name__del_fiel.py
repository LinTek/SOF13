# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Worker.username'
        db.delete_column(u'functionary_worker', 'username')

        # Deleting field 'Worker.first_name'
        db.delete_column(u'functionary_worker', 'first_name')

        # Deleting field 'Worker.last_name'
        db.delete_column(u'functionary_worker', 'last_name')

        # Deleting field 'Worker.is_staff'
        db.delete_column(u'functionary_worker', 'is_staff')

        # Deleting field 'Worker.pid'
        db.delete_column(u'functionary_worker', 'pid')

        # Deleting field 'Worker.is_active'
        db.delete_column(u'functionary_worker', 'is_active')

        # Deleting field 'Worker.id'
        db.delete_column(u'functionary_worker', u'id')

        # Deleting field 'Worker.is_superuser'
        db.delete_column(u'functionary_worker', 'is_superuser')

        # Deleting field 'Worker.last_login'
        db.delete_column(u'functionary_worker', 'last_login')

        # Deleting field 'Worker.password'
        db.delete_column(u'functionary_worker', 'password')

        # Deleting field 'Worker.email'
        db.delete_column(u'functionary_worker', 'email')

        # Deleting field 'Worker.date_joined'
        db.delete_column(u'functionary_worker', 'date_joined')

        # Removing M2M table for field groups on 'Worker'
        db.delete_table('functionary_worker_groups')

        # Removing M2M table for field user_permissions on 'Worker'
        db.delete_table('functionary_worker_user_permissions')


        # Changing field 'Worker.person_ptr'
        db.alter_column(u'functionary_worker', u'person_ptr_id', self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['functionary.Person'], unique=True, primary_key=True))

        # Changing field 'Person.last_name'
        db.alter_column(u'functionary_person', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=40))

        # Changing field 'Person.email'
        db.alter_column(u'functionary_person', 'email', self.gf('django.db.models.fields.EmailField')(max_length=50))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Worker.username'
        raise RuntimeError("Cannot reverse this migration. 'Worker.username' and its values cannot be restored.")
        # Adding field 'Worker.first_name'
        db.add_column(u'functionary_worker', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'Worker.last_name'
        db.add_column(u'functionary_worker', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'Worker.is_staff'
        db.add_column(u'functionary_worker', 'is_staff',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Worker.pid'
        raise RuntimeError("Cannot reverse this migration. 'Worker.pid' and its values cannot be restored.")
        # Adding field 'Worker.is_active'
        db.add_column(u'functionary_worker', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Worker.id'
        raise RuntimeError("Cannot reverse this migration. 'Worker.id' and its values cannot be restored.")
        # Adding field 'Worker.is_superuser'
        db.add_column(u'functionary_worker', 'is_superuser',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Worker.last_login'
        db.add_column(u'functionary_worker', 'last_login',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Worker.password'
        raise RuntimeError("Cannot reverse this migration. 'Worker.password' and its values cannot be restored.")
        # Adding field 'Worker.email'
        db.add_column(u'functionary_worker', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True),
                      keep_default=False)

        # Adding field 'Worker.date_joined'
        db.add_column(u'functionary_worker', 'date_joined',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding M2M table for field groups on 'Worker'
        db.create_table(u'functionary_worker_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('worker', models.ForeignKey(orm[u'functionary.worker'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'functionary_worker_groups', ['worker_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Worker'
        db.create_table(u'functionary_worker_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('worker', models.ForeignKey(orm[u'functionary.worker'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'functionary_worker_user_permissions', ['worker_id', 'permission_id'])


        # Changing field 'Worker.person_ptr'
        db.alter_column(u'functionary_worker', 'person_ptr_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['functionary.Person'], unique=True, null=True))

        # Changing field 'Person.last_name'
        db.alter_column(u'functionary_person', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Person.email'
        db.alter_column(u'functionary_person', 'email', self.gf('django.db.models.fields.EmailField')(max_length=20))

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
            'contract_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['functionary.Person']", 'unique': 'True', 'primary_key': 'True'}),
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