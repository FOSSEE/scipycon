# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Wifi'
        db.create_table('registration_wifi', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scope', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Event'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('wifi', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('registration', ['Wifi'])

        # Adding model 'Accommodation'
        db.create_table('registration_accommodation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scope', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Event'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('accommodation_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accommodation_days', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('registration', ['Accommodation'])

        # Adding model 'Registration'
        db.create_table('registration_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scope', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Event'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('registrant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('organisation', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('phone_num', self.gf('django.db.models.fields.CharField')(max_length=14, blank=True)),
            ('tshirt', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('conference', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tutorial', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sprint', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('final_conference', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('final_tutorial', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('final_sprint', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_contact', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_mod', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('registration', ['Registration'])


    def backwards(self, orm):
        
        # Deleting model 'Wifi'
        db.delete_table('registration_wifi')

        # Deleting model 'Accommodation'
        db.delete_table('registration_accommodation')

        # Deleting model 'Registration'
        db.delete_table('registration_registration')


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
        'base.event': {
            'Meta': {'object_name': 'Event'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'turn': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'registration.accommodation': {
            'Meta': {'object_name': 'Accommodation'},
            'accommodation_days': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'accommodation_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Event']"}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'registration.registration': {
            'Meta': {'object_name': 'Registration'},
            'allow_contact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conference': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'final_conference': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'final_sprint': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'final_tutorial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_mod': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'phone_num': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'registrant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'scope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Event']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sprint': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tshirt': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'tutorial': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'registration.wifi': {
            'Meta': {'object_name': 'Wifi'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Event']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'wifi': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['registration']
