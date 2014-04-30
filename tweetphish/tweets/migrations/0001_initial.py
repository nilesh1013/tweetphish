# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TweetUrls'
        db.create_table(u'tweets_tweeturls', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=2000, unique=True, null=True, blank=True)),
            ('phish_url', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('users', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tags', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('which_phish', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('full_url', self.gf('django.db.models.fields.URLField')(max_length=2000, null=True, blank=True)),
        ))
        db.send_create_signal(u'tweets', ['TweetUrls'])


    def backwards(self, orm):
        # Deleting model 'TweetUrls'
        db.delete_table(u'tweets_tweeturls')


    models = {
        u'tweets.tweeturls': {
            'Meta': {'object_name': 'TweetUrls'},
            'full_url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phish_url': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'which_phish': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tweets']