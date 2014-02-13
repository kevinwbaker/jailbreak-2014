# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'University'
        db.create_table('teams_university', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('teams', ['University'])

        # Adding model 'Team'
        db.create_table('teams_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('sponsor_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.University'])),
            ('long_position', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('lat_position', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
        ))
        db.send_create_signal('teams', ['Team'])


    def backwards(self, orm):
        # Deleting model 'University'
        db.delete_table('teams_university')

        # Deleting model 'Team'
        db.delete_table('teams_team')


    models = {
        'teams.team': {
            'Meta': {'object_name': 'Team'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_position': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'long_position': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sponsor_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.University']"})
        },
        'teams.university': {
            'Meta': {'object_name': 'University'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['teams']