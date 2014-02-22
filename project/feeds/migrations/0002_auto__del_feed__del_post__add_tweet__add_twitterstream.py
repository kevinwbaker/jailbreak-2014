# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table(u'feeds_feed')

        # Deleting model 'Post'
        db.delete_table(u'feeds_post')

        # Adding model 'Tweet'
        db.create_table(u'feeds_tweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweet_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('media_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('in_reply_to_user_name', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('retweeted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('user_photo', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('user_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tweets', null=True, to=orm['teams.Team'])),
        ))
        db.send_create_signal(u'feeds', ['Tweet'])

        # Adding model 'TwitterStream'
        db.create_table(u'feeds_twitterstream', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('stream_id', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=128)),
            ('include_rts', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='feeds', null=True, to=orm['teams.Team'])),
        ))
        db.send_create_signal(u'feeds', ['TwitterStream'])


    def backwards(self, orm):
        # Adding model 'Feed'
        db.create_table(u'feeds_feed', (
            ('feed_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('source', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feeds', null=True, to=orm['teams.Team'])),
        ))
        db.send_create_signal(u'feeds', ['Feed'])

        # Adding model 'Post'
        db.create_table(u'feeds_post', (
            ('user_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_photo', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('media', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('source', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', null=True, to=orm['teams.Team'])),
        ))
        db.send_create_signal(u'feeds', ['Post'])

        # Deleting model 'Tweet'
        db.delete_table(u'feeds_tweet')

        # Deleting model 'TwitterStream'
        db.delete_table(u'feeds_twitterstream')


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
            'tweet_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'user_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user_photo': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'feeds.twitterstream': {
            'Meta': {'object_name': 'TwitterStream'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_rts': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'stream_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '128'}),
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