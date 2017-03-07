# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Corporate'
        db.create_table('appsite_corporate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('superior_text', self.gf('django.db.models.fields.TextField')()),
            ('lower_text', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('video', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('appsite', ['Corporate'])

        # Adding model 'PrivacyPolicy'
        db.create_table('appsite_privacypolicy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('appsite', ['PrivacyPolicy'])

        # Adding model 'TermsOfUse'
        db.create_table('appsite_termsofuse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('appsite', ['TermsOfUse'])


    def backwards(self, orm):
        
        # Deleting model 'Corporate'
        db.delete_table('appsite_corporate')

        # Deleting model 'PrivacyPolicy'
        db.delete_table('appsite_privacypolicy')

        # Deleting model 'TermsOfUse'
        db.delete_table('appsite_termsofuse')


    models = {
        'appsite.corporate': {
            'Meta': {'object_name': 'Corporate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lower_text': ('django.db.models.fields.TextField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'superior_text': ('django.db.models.fields.TextField', [], {}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'appsite.privacypolicy': {
            'Meta': {'object_name': 'PrivacyPolicy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'appsite.termsofuse': {
            'Meta': {'object_name': 'TermsOfUse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['appsite']
