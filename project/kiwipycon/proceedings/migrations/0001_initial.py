# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from project.kiwipycon.proceedings.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Paper'
        db.create_table('proceedings_paper', (
            ('body', models.TextField()),
            ('abstract', models.TextField()),
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(max_length=200)),
        ))
        db.send_create_signal('proceedings', ['Paper'])
        
        # Adding model 'Attachments'
        db.create_table('proceedings_attachments', (
            ('paper', models.ForeignKey(orm.Paper)),
            ('id', models.AutoField(primary_key=True)),
            ('attachments', models.FileField(upload_to='attachments/%Y/%m/%d')),
        ))
        db.send_create_signal('proceedings', ['Attachments'])
        
        # Adding ManyToManyField 'Paper.authors'
        db.create_table('proceedings_paper_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('paper', models.ForeignKey(Paper, null=False)),
            ('user', models.ForeignKey(User, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Paper'
        db.delete_table('proceedings_paper')
        
        # Deleting model 'Attachments'
        db.delete_table('proceedings_attachments')
        
        # Dropping ManyToManyField 'Paper.authors'
        db.delete_table('proceedings_paper_authors')
        
    
    
    models = {
        'proceedings.paper': {
            'abstract': ('models.TextField', [], {}),
            'authors': ('models.ManyToManyField', ['User'], {}),
            'body': ('models.TextField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('models.CharField', [], {'max_length': '200'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'proceedings.attachments': {
            'attachments': ('models.FileField', [], {'upload_to': "'attachments/%Y/%m/%d'"}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'paper': ('models.ForeignKey', ['Paper'], {})
        }
    }
    
    complete_apps = ['proceedings']
