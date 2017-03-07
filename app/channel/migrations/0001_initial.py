# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Video'
        db.create_table('channel_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['category.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length='128')),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('video', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.City'])),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32, db_index=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 3, 6, 12, 55, 6, 418424))),
            ('date_expires', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_national', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('channel', ['Video'])


    def backwards(self, orm):
        
        # Deleting model 'Video'
        db.delete_table('channel_video')


    models = {
        'category.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_top_ten': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'channel.video': {
            'Meta': {'object_name': 'Video'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.Category']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.City']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 3, 6, 12, 55, 6, 418424)'}),
            'date_expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'is_national': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'128'"}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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

    complete_apps = ['channel']
