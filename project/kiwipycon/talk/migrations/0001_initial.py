# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from project.kiwipycon.talk.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Talk'
        db.create_table('talk_talk', (
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField()),
            ('speaker', models.ForeignKey(orm['auth.User'])),
            ('authors_bio', models.TextField()),
            ('contact', models.CharField(max_length=1024)),
            ('title', models.CharField(max_length=1024)),
            ('abstract', models.TextField()),
            ('outline', models.TextField()),
            ('topic', models.CharField(blank=True, max_length=255)),
            ('topic_other', models.CharField(max_length=255, blank=True)),
            ('duration', models.CharField(max_length=3)),
            ('audience', models.CharField(blank=True, max_length=32)),
            ('audience_other', models.CharField(max_length=128, blank=True)),
            ('approved', models.BooleanField(default=False)),
            ('submitted', models.DateTimeField(auto_now_add=True)),
            ('last_mod', models.DateTimeField(auto_now=True)),
            ('tags', TagField(blank=True)),
        ))
        db.send_create_signal('talk', ['Talk'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Talk'
        db.delete_table('talk_talk')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'talk.talk': {
            'abstract': ('models.TextField', [], {}),
            'approved': ('models.BooleanField', [], {'default': 'False'}),
            'audience': ('models.CharField', [], {'blank': 'True', 'max_length': '32'}),
            'audience_other': ('models.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'authors_bio': ('models.TextField', [], {}),
            'contact': ('models.CharField', [], {'max_length': '1024'}),
            'duration': ('models.CharField', [], {'max_length': '3'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'last_mod': ('models.DateTimeField', [], {'auto_now': 'True'}),
            'outline': ('models.TextField', [], {}),
            'slug': ('models.SlugField', [], {}),
            'speaker': ('models.ForeignKey', ['User'], {}),
            'submitted': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'tags': ('TagField', [], {'blank': 'True'}),
            'title': ('models.CharField', [], {'max_length': '1024'}),
            'topic': ('models.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'topic_other': ('models.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }
    
    complete_apps = ['talk']
