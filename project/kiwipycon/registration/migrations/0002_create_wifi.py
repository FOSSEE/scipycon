# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from project.kiwipycon.registration.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Wifi'
        db.create_table('registration_wifi', (
            ('wifi', models.CharField(max_length=50)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('registration', ['Wifi'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Wifi'
        db.delete_table('registration_wifi')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'registration.wifi': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'user': ('models.ForeignKey', ['User'], {}),
            'wifi': ('models.CharField', [], {'max_length': '50'})
        },
        'registration.registration': {
            'allow_contact': ('models.BooleanField', [], {'default': 'False'}),
            'amount': ('models.IntegerField', [], {'default': '0'}),
            'beverage': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'diet': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'discount': ('models.BooleanField', [], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'last_mod': ('models.DateTimeField', [], {'auto_now': 'True'}),
            'occupation': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'organisation': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'party': ('models.BooleanField', [], {'default': 'False'}),
            'payment': ('models.BooleanField', [], {'default': 'False'}),
            'postcode': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'registrant': ('models.ForeignKey', ['User'], {}),
            'slug': ('models.SlugField', [], {}),
            'sponsor': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'submitted': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'tshirt': ('models.CharField', [], {'max_length': '2'})
        }
    }
    
    complete_apps = ['registration']
