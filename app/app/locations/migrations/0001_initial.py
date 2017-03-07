# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'State'
        db.create_table('locations_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('locations', ['State'])

        # Adding model 'City'
        db.create_table('locations_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.State'])),
        ))
        db.send_create_signal('locations', ['City'])

        # Adding model 'Area'
        db.create_table('locations_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.City'])),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('locations', ['Area'])

        # Adding model 'ZipCode'
        db.create_table('locations_zipcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.City'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Area'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('locations', ['ZipCode'])


    def backwards(self, orm):
        
        # Deleting model 'State'
        db.delete_table('locations_state')

        # Deleting model 'City'
        db.delete_table('locations_city')

        # Deleting model 'Area'
        db.delete_table('locations_area')

        # Deleting model 'ZipCode'
        db.delete_table('locations_zipcode')


    models = {
        'locations.area': {
            'Meta': {'ordering': "('area',)", 'object_name': 'Area'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'locations.city': {
            'Meta': {'ordering': "('city',)", 'object_name': 'City'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.State']"})
        },
        'locations.state': {
            'Meta': {'ordering': "('state',)", 'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'locations.zipcode': {
            'Meta': {'ordering': "('zip_code',)", 'object_name': 'ZipCode'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Area']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        }
    }

    complete_apps = ['locations']
