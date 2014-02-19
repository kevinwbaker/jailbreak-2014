# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table(u'teams_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('cover_photo', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('sponsor_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('donate_reason', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('amount_raised', self.gf('django.db.models.fields.IntegerField')()),
            ('university', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'teams', ['Team'])

        # Adding model 'Checkin'
        db.create_table(u'teams_checkin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lng_position', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('lat_position', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='checkins', to=orm['teams.Team'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal(u'teams', ['Checkin'])


    def backwards(self, orm):
        # Deleting model 'Team'
        db.delete_table(u'teams_team')

        # Deleting model 'Checkin'
        db.delete_table(u'teams_checkin')


    models = {
        u'teams.checkin': {
            'Meta': {'object_name': 'Checkin'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_position': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'lng_position': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checkins'", 'to': u"orm['teams.Team']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'amount_raised': ('django.db.models.fields.IntegerField', [], {}),
            'cover_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'donate_reason': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sponsor_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'university': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['teams']