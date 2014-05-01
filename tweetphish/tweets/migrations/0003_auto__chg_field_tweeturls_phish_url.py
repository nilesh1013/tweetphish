# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TweetUrls.phish_url'
        db.alter_column(u'tweets_tweeturls', 'phish_url', self.gf('django.db.models.fields.NullBooleanField')(null=True))

    def backwards(self, orm):

        # Changing field 'TweetUrls.phish_url'
        db.alter_column(u'tweets_tweeturls', 'phish_url', self.gf('django.db.models.fields.BooleanField')())

    models = {
        u'tweets.tweeturls': {
            'Meta': {'object_name': 'TweetUrls'},
            'full_url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phish_url': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'query_keyword': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user_keyword': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'which_phish': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tweets']