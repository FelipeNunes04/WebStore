# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Banner'
        db.create_table('banner_banner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['category.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.City'])),
            ('target', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 3, 6, 12, 54, 29, 545911))),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 3, 6, 12, 54, 29, 545940))),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_national', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('banner', ['Banner'])

        # Adding model 'CarouselHome'
        db.create_table('banner_carouselhome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.City'])),
            ('target', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 3, 6, 12, 54, 29, 546845))),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 3, 6, 12, 54, 29, 546871))),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_national', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('banner', ['CarouselHome'])


    def backwards(self, orm):
        
        # Deleting model 'Banner'
        db.delete_table('banner_banner')

        # Deleting model 'CarouselHome'
        db.delete_table('banner_carouselhome')


    models = {
        'banner.banner': {
            'Meta': {'object_name': 'Banner'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.Category']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.City']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 3, 6, 12, 54, 29, 545911)'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_national': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 3, 6, 12, 54, 29, 545940)'}),
            'target': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'banner.carouselhome': {
            'Meta': {'object_name': 'CarouselHome'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.City']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 3, 6, 12, 54, 29, 546845)'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_national': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 3, 6, 12, 54, 29, 546871)'}),
            'target': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'category.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_top_ten': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
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
        }
    }

    complete_apps = ['banner']
