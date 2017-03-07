# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Question'
        db.create_table('polls_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.City'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_national', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('polls', ['Question'])

        # Adding model 'Choice'
        db.create_table('polls_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Question'])),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('polls', ['Choice'])

        # Adding model 'Vote'
        db.create_table('polls_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Question'])),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Choice'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal('polls', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['question', 'ip']
        db.create_unique('polls_vote', ['question_id', 'ip'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Vote', fields ['question', 'ip']
        db.delete_unique('polls_vote', ['question_id', 'ip'])

        # Deleting model 'Question'
        db.delete_table('polls_question')

        # Deleting model 'Choice'
        db.delete_table('polls_choice')

        # Deleting model 'Vote'
        db.delete_table('polls_vote')


    models = {
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
        'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Question']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'polls.question': {
            'Meta': {'object_name': 'Question'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.City']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_national': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'polls.vote': {
            'Meta': {'unique_together': "(('question', 'ip'),)", 'object_name': 'Vote'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Choice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Question']"})
        }
    }

    complete_apps = ['polls']
