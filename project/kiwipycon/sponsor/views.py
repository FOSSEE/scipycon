# -*- coding: utf-8 -*-
from __future__ import absolute_import

# django
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

def schwag_sponsors(request,
        template_name = 'sponsor/schwag.html'):
    """Simple page to display schwag sponsors
    
    The list is generated in kiwipycon.context_processors
    """
    return render_to_response(template_name, RequestContext(request,
        {}))

