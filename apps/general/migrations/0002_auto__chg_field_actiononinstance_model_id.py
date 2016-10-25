# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ActionOnInstance.model_id'
        db.alter_column(u'general_actiononinstance', 'model_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'ActionOnInstance.model_id'
        db.alter_column(u'general_actiononinstance', 'model_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=-1))

    models = {
        u'general.actiononinstance': {
            'Meta': {'object_name': 'ActionOnInstance'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.TextField', [], {}),
            'model_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['general']
