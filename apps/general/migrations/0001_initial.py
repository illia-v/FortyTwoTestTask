# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActionOnInstance'
        db.create_table(u'general_actiononinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('model_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('instance', self.gf('django.db.models.fields.TextField')()),
            ('action', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'general', ['ActionOnInstance'])


    def backwards(self, orm):
        # Deleting model 'ActionOnInstance'
        db.delete_table(u'general_actiononinstance')


    models = {
        u'general.actiononinstance': {
            'Meta': {'object_name': 'ActionOnInstance'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.TextField', [], {}),
            'model_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['general']