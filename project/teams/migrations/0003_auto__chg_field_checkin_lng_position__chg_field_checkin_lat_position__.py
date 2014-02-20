# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Checkin.lng_position'
        db.alter_column(u'teams_checkin', 'lng_position', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=4))

        # Changing field 'Checkin.lat_position'
        db.alter_column(u'teams_checkin', 'lat_position', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=4))
        # Adding field 'Team.start_lat'
        db.add_column(u'teams_team', 'start_lat',
                      self.gf('django.db.models.fields.DecimalField')(default=53.3418701, max_digits=8, decimal_places=4),
                      keep_default=False)

        # Adding field 'Team.start_lng'
        db.add_column(u'teams_team', 'start_lng',
                      self.gf('django.db.models.fields.DecimalField')(default=-6.3098048, max_digits=8, decimal_places=4),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Checkin.lng_position'
        db.alter_column(u'teams_checkin', 'lng_position', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Checkin.lat_position'
        db.alter_column(u'teams_checkin', 'lat_position', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))
        # Deleting field 'Team.start_lat'
        db.delete_column(u'teams_team', 'start_lat')

        # Deleting field 'Team.start_lng'
        db.delete_column(u'teams_team', 'start_lng')


    models = {
        u'teams.checkin': {
            'Meta': {'object_name': 'Checkin'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_position': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '4'}),
            'lng_position': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '4'}),
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
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sponsor_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'start_lat': ('django.db.models.fields.DecimalField', [], {'default': '53.3418701', 'max_digits': '8', 'decimal_places': '4'}),
            'start_lng': ('django.db.models.fields.DecimalField', [], {'default': '-6.3098048', 'max_digits': '8', 'decimal_places': '4'}),
            'university': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'db_index': 'True'})
        }
    }

    complete_apps = ['teams']