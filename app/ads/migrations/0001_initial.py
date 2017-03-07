# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Plan'
        db.create_table('ads_plan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('days', self.gf('django.db.models.fields.IntegerField')()),
            ('value_ad', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('ads', ['Plan'])

        # Adding model 'Signature'
        db.create_table('ads_signature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ads.Plan'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customer.Advertiser'])),
            ('number_ads', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3)),
            ('value_signature', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('number_ads_available', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 3, 6, 12, 50, 11, 554509))),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ads', ['Signature'])

        # Adding model 'Ad'
        db.create_table('ads_ad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['category.Category'])),
            ('signature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ads.Signature'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customer.Advertiser'])),
            ('type_ad', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('fancy_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('video', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64, db_index=True)),
            ('time_working', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('complement', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.State'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.City'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Area'], null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('is_national', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('ads', ['Ad'])

        # Adding M2M table for field activities on 'Ad'
        db.create_table('ads_ad_activities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ad', models.ForeignKey(orm['ads.ad'], null=False)),
            ('activity', models.ForeignKey(orm['category.activity'], null=False))
        ))
        db.create_unique('ads_ad_activities', ['ad_id', 'activity_id'])

        # Adding M2M table for field option_values on 'Ad'
        db.create_table('ads_ad_option_values', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ad', models.ForeignKey(orm['ads.ad'], null=False)),
            ('optionvalue', models.ForeignKey(orm['category.optionvalue'], null=False))
        ))
        db.create_unique('ads_ad_option_values', ['ad_id', 'optionvalue_id'])

        # Adding M2M table for field payment on 'Ad'
        db.create_table('ads_ad_payment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ad', models.ForeignKey(orm['ads.ad'], null=False)),
            ('payment', models.ForeignKey(orm['payment.payment'], null=False))
        ))
        db.create_unique('ads_ad_payment', ['ad_id', 'payment_id'])

        # Adding model 'Photo'
        db.create_table('ads_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ads.Ad'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('ads', ['Photo'])


    def backwards(self, orm):
        
        # Deleting model 'Plan'
        db.delete_table('ads_plan')

        # Deleting model 'Signature'
        db.delete_table('ads_signature')

        # Deleting model 'Ad'
        db.delete_table('ads_ad')

        # Removing M2M table for field activities on 'Ad'
        db.delete_table('ads_ad_activities')

        # Removing M2M table for field option_values on 'Ad'
        db.delete_table('ads_ad_option_values')

        # Removing M2M table for field payment on 'Ad'
        db.delete_table('ads_ad_payment')

        # Deleting model 'Photo'
        db.delete_table('ads_photo')


    models = {
        'ads.ad': {
            'Meta': {'object_name': 'Ad'},
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['category.Activity']", 'symmetrical': 'False'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Area']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.Category']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.City']"}),
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'fancy_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_national': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'option_values': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['category.OptionValue']", 'symmetrical': 'False'}),
            'payment': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['payment.Payment']", 'symmetrical': 'False'}),
            'signature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.Signature']"}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.State']"}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'time_working': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type_ad': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.Advertiser']"}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'ads.photo': {
            'Meta': {'object_name': 'Photo'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.Ad']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'ads.plan': {
            'Meta': {'object_name': 'Plan'},
            'days': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value_ad': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'})
        },
        'ads.signature': {
            'Meta': {'object_name': 'Signature'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.Advertiser']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_ads': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'number_ads_available': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.Plan']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 3, 6, 12, 50, 11, 554509)'}),
            'value_signature': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'})
        },
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
        },
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
        'payment.payment': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Payment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['ads']
