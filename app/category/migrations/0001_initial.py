# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('category_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('image_top_ten', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('category', ['Category'])

        # Adding model 'OptionGroup'
        db.create_table('category_optiongroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name_admin', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('category', ['OptionGroup'])

        # Adding model 'OptionValue'
        db.create_table('category_optionvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['category.OptionGroup'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('category', ['OptionValue'])

        # Adding model 'Activity'
        db.create_table('category_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('category', ['Activity'])

        # Adding M2M table for field categories on 'Activity'
        db.create_table('category_activity_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['category.activity'], null=False)),
            ('category', models.ForeignKey(orm['category.category'], null=False))
        ))
        db.create_unique('category_activity_categories', ['activity_id', 'category_id'])

        # Adding M2M table for field option_groups on 'Activity'
        db.create_table('category_activity_option_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['category.activity'], null=False)),
            ('optiongroup', models.ForeignKey(orm['category.optiongroup'], null=False))
        ))
        db.create_unique('category_activity_option_groups', ['activity_id', 'optiongroup_id'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('category_category')

        # Deleting model 'OptionGroup'
        db.delete_table('category_optiongroup')

        # Deleting model 'OptionValue'
        db.delete_table('category_optionvalue')

        # Deleting model 'Activity'
        db.delete_table('category_activity')

        # Removing M2M table for field categories on 'Activity'
        db.delete_table('category_activity_categories')

        # Removing M2M table for field option_groups on 'Activity'
        db.delete_table('category_activity_option_groups')


    models = {
        'category.activity': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Activity'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['category.Category']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'option_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['category.OptionGroup']", 'symmetrical': 'False'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
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
        'category.optiongroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'OptionGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_admin': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'category.optionvalue': {
            'Meta': {'ordering': "('name',)", 'object_name': 'OptionValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'option_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.OptionGroup']"}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['category']
