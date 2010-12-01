
from south.db import db
from django.db import models
from project.scipycon.registration.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Wifi'
        db.create_table('registration_wifi', (
            ('id', orm['registration.Wifi:id']),
            ('scope', orm['registration.Wifi:scope']),
            ('user', orm['registration.Wifi:user']),
            ('wifi', orm['registration.Wifi:wifi']),
            ('registration_id', orm['registration.Wifi:registration_id']),
        ))
        db.send_create_signal('registration', ['Wifi'])
        
        # Adding model 'Accommodation'
        db.create_table('registration_accommodation', (
            ('id', orm['registration.Accommodation:id']),
            ('scope', orm['registration.Accommodation:scope']),
            ('user', orm['registration.Accommodation:user']),
            ('sex', orm['registration.Accommodation:sex']),
            ('accommodation_required', orm['registration.Accommodation:accommodation_required']),
            ('accommodation_on_1st', orm['registration.Accommodation:accommodation_on_1st']),
            ('accommodation_on_2nd', orm['registration.Accommodation:accommodation_on_2nd']),
            ('accommodation_on_3rd', orm['registration.Accommodation:accommodation_on_3rd']),
            ('accommodation_on_4th', orm['registration.Accommodation:accommodation_on_4th']),
            ('accommodation_on_5th', orm['registration.Accommodation:accommodation_on_5th']),
            ('accommodation_on_6th', orm['registration.Accommodation:accommodation_on_6th']),
            ('accommodation_days', orm['registration.Accommodation:accommodation_days']),
        ))
        db.send_create_signal('registration', ['Accommodation'])
        
        # Adding model 'Payment'
        db.create_table('registration_payment', (
            ('id', orm['registration.Payment:id']),
            ('scope', orm['registration.Payment:scope']),
            ('user', orm['registration.Payment:user']),
            ('confirmed', orm['registration.Payment:confirmed']),
            ('acco_confirmed', orm['registration.Payment:acco_confirmed']),
            ('date_confirmed', orm['registration.Payment:date_confirmed']),
            ('confirmed_mail', orm['registration.Payment:confirmed_mail']),
            ('acco_confirmed_mail', orm['registration.Payment:acco_confirmed_mail']),
            ('type', orm['registration.Payment:type']),
            ('details', orm['registration.Payment:details']),
        ))
        db.send_create_signal('registration', ['Payment'])
        
        # Adding model 'Registration'
        db.create_table('registration_registration', (
            ('id', orm['registration.Registration:id']),
            ('scope', orm['registration.Registration:scope']),
            ('slug', orm['registration.Registration:slug']),
            ('registrant', orm['registration.Registration:registrant']),
            ('organisation', orm['registration.Registration:organisation']),
            ('occupation', orm['registration.Registration:occupation']),
            ('city', orm['registration.Registration:city']),
            ('postcode', orm['registration.Registration:postcode']),
            ('phone_num', orm['registration.Registration:phone_num']),
            ('tshirt', orm['registration.Registration:tshirt']),
            ('conference', orm['registration.Registration:conference']),
            ('tutorial', orm['registration.Registration:tutorial']),
            ('sprint', orm['registration.Registration:sprint']),
            ('final_conference', orm['registration.Registration:final_conference']),
            ('final_tutorial', orm['registration.Registration:final_tutorial']),
            ('final_sprint', orm['registration.Registration:final_sprint']),
            ('allow_contact', orm['registration.Registration:allow_contact']),
            ('submitted', orm['registration.Registration:submitted']),
            ('last_mod', orm['registration.Registration:last_mod']),
        ))
        db.send_create_signal('registration', ['Registration'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Wifi'
        db.delete_table('registration_wifi')
        
        # Deleting model 'Accommodation'
        db.delete_table('registration_accommodation')
        
        # Deleting model 'Payment'
        db.delete_table('registration_payment')
        
        # Deleting model 'Registration'
        db.delete_table('registration_registration')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'base.event': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'turn': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'registration.accommodation': {
            'accommodation_days': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'accommodation_on_1st': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'accommodation_on_2nd': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'accommodation_on_3rd': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'accommodation_on_4th': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'accommodation_on_5th': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'accommodation_on_6th': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'accommodation_required': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Event']"}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'registration.payment': {
            'acco_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'acco_confirmed_mail': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'confirmed_mail': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'date_confirmed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Event']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'registration.registration': {
            'allow_contact': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conference': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'final_conference': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'final_sprint': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'final_tutorial': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_mod': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'phone_num': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'registrant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'scope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Event']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sprint': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tshirt': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'tutorial': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'registration.wifi': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'scope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Event']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'wifi': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['registration']
