# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from project.kiwipycon.user.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('user_userprofile', (
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'], unique=True)),
            ('url', models.URLField(verify_exists=False, blank=True)),
            ('photo', models.CharField(max_length=64, blank=True)),
            ('about', models.TextField(blank=True)),
        ))
        db.send_create_signal('user', ['UserProfile'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('user_userprofile')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'user.userprofile': {
            'about': ('models.TextField', [], {'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'photo': ('models.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'url': ('models.URLField', [], {'verify_exists': 'False', 'blank': 'True'}),
            'user': ('models.ForeignKey', ['User'], {'unique': 'True'})
        }
    }
    
    complete_apps = ['user']
