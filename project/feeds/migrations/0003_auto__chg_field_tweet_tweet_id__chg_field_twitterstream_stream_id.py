# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tweet.tweet_id'
        db.alter_column(u'feeds_tweet', 'tweet_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True))

        # Changing field 'TwitterStream.stream_id'
        db.alter_column(u'feeds_twitterstream', 'stream_id', self.gf('django.db.models.fields.BigIntegerField')(max_length=128))

    def backwards(self, orm):

        # Changing field 'Tweet.tweet_id'
        db.alter_column(u'feeds_tweet', 'tweet_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True))

        # Changing field 'TwitterStream.stream_id'
        db.alter_column(u'feeds_twitterstream', 'stream_id', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=128))

    models = {
        u'feeds.tweet': {
            'Meta': {'object_name': 'Tweet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_reply_to_user_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'media_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'retweeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tweets'", 'null': 'True', 'to': u"orm['teams.Team']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'user_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user_photo': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'feeds.twitterstream': {
            'Meta': {'object_name': 'TwitterStream'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_rts': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'stream_id': ('django.db.models.fields.BigIntegerField', [], {'max_length': '128'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'feeds'", 'null': 'True', 'to': u"orm['teams.Team']"}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'amount_raised': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sponsor_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'start_lat': ('django.db.models.fields.DecimalField', [], {'default': "'53.3418'", 'max_digits': '8', 'decimal_places': '4'}),
            'start_lng': ('django.db.models.fields.DecimalField', [], {'default': "'-6.3098'", 'max_digits': '8', 'decimal_places': '4'}),
            'university': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'youtube_embed_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['feeds']