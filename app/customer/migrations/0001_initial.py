# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('customer_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('complement', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
            ('is_advertiser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('area_cell_phone', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('cell_phone', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('customer', ['UserProfile'])

        # Adding model 'Customer'
        db.create_table('customer_customer', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['customer.UserProfile'], unique=True, primary_key=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('area_phone', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('newsletter', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('customer', ['Customer'])

        # Adding M2M table for field interest_area on 'Customer'
        db.create_table('customer_customer_interest_area', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['customer.customer'], null=False)),
            ('category', models.ForeignKey(orm['category.category'], null=False))
        ))
        db.create_unique('customer_customer_interest_area', ['customer_id', 'category_id'])

        # Adding model 'Advertiser'
        db.create_table('customer_advertiser', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['customer.UserProfile'], unique=True, primary_key=True)),
            ('fancy_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('area_phone', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('type_person', self.gf('django.db.models.fields.CharField')(default='legal_entity', max_length=16)),
            ('cpf_cnpj', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('responsible', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('customer', ['Advertiser'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('customer_userprofile')

        # Deleting model 'Customer'
        db.delete_table('customer_customer')

        # Removing M2M table for field interest_area on 'Customer'
        db.delete_table('customer_customer_interest_area')

        # Deleting model 'Advertiser'
        db.delete_table('customer_advertiser')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customer.advertiser': {
            'Meta': {'object_name': 'Advertiser', '_ormbases': ['customer.UserProfile']},
            'area_phone': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'cpf_cnpj': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'fancy_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'responsible': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type_person': ('django.db.models.fields.CharField', [], {'default': "'legal_entity'", 'max_length': '16'}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['customer.UserProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        'customer.customer': {
            'Meta': {'object_name': 'Customer', '_ormbases': ['customer.UserProfile']},
            'area_phone': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'interest_area': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['customer.UserProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        'customer.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'area_cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_advertiser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['customer']
