# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from project.kiwipycon.registration.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Registration'
        db.create_table('registration_registration', (
            ('city', models.CharField(max_length=255, blank=True)),
            ('slug', models.SlugField()),
            ('submitted', models.DateTimeField(auto_now_add=True)),
            ('allow_contact', models.BooleanField(default=False)),
            ('last_mod', models.DateTimeField(auto_now=True)),
            ('payment', models.BooleanField(default=False)),
            ('organisation', models.CharField(max_length=255, blank=True)),
            ('diet', models.CharField(max_length=255, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('sponsor', models.CharField(max_length=255, blank=True)),
            ('discount', models.BooleanField(default=False)),
            ('amount', models.IntegerField(default=0)),
            ('tshirt', models.CharField(max_length=2)),
            ('beverage', models.CharField(max_length=255, blank=True)),
            ('postcode', models.CharField(max_length=255, blank=True)),
            ('party', models.BooleanField(default=False)),
            ('registrant', models.ForeignKey(orm['auth.User'])),
            ('occupation', models.CharField(max_length=255, blank=True)),
        ))
        db.send_create_signal('registration', ['Registration'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Registration'
        db.delete_table('registration_registration')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'registration.registration': {
            'allow_contact': ('models.BooleanField', [], {'default': 'False'}),
            'beverage': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'diet': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'discount': ('models.BooleanField', [], {'default': 'False'}),
            'amount': ('models.IntegerField', [], {'default': 0}),
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
