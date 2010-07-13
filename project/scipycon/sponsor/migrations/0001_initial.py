# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from project.kiwipycon.sponsor.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Sponsor'
        db.create_table('sponsor_sponsor', (
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField()),
            ('title', models.CharField(max_length=255)),
            ('type', models.CharField(max_length=10)),
            ('url', models.URLField(verify_exists=False, blank=True)),
            ('contact_name', models.CharField(max_length=255)),
            ('contact_phone', models.CharField(max_length=255)),
            ('contact_email', models.CharField(max_length=255)),
            ('logo', models.CharField(max_length=64, blank=True)),
            ('guests', models.IntegerField()),
        ))
        db.send_create_signal('sponsor', ['Sponsor'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Sponsor'
        db.delete_table('sponsor_sponsor')
        
    
    
    models = {
        'sponsor.sponsor': {
            'contact_email': ('models.CharField', [], {'max_length': '255'}),
            'contact_name': ('models.CharField', [], {'max_length': '255'}),
            'contact_phone': ('models.CharField', [], {'max_length': '255'}),
            'guests': ('models.IntegerField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'logo': ('models.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {}),
            'title': ('models.CharField', [], {'max_length': '255'}),
            'type': ('models.CharField', [], {'max_length': '10'}),
            'url': ('models.URLField', [], {'verify_exists': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['sponsor']
