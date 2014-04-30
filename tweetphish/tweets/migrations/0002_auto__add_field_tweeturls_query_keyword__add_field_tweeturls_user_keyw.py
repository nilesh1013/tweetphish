# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TweetUrls.query_keyword'
        db.add_column(u'tweets_tweeturls', 'query_keyword',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TweetUrls.user_keyword'
        db.add_column(u'tweets_tweeturls', 'user_keyword',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TweetUrls.query_keyword'
        db.delete_column(u'tweets_tweeturls', 'query_keyword')

        # Deleting field 'TweetUrls.user_keyword'
        db.delete_column(u'tweets_tweeturls', 'user_keyword')


    models = {
        u'tweets.tweeturls': {
            'Meta': {'object_name': 'TweetUrls'},
            'full_url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phish_url': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'query_keyword': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user_keyword': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'which_phish': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tweets']