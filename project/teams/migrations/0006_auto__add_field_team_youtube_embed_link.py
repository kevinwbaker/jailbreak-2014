# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Team.youtube_embed_link'
        db.add_column(u'teams_team', 'youtube_embed_link',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Team.youtube_embed_link'
        db.delete_column(u'teams_team', 'youtube_embed_link')


    models = {
        u'teams.checkin': {
            'Meta': {'object_name': 'Checkin'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_position': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '4'}),
            'lng_position': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '4'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checkins'", 'to': u"orm['teams.Team']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
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

    complete_apps = ['teams']