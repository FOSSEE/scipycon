# -*- coding: utf-8 -*-
#python
import urllib
import datetime
import re
from random import randint

#django
from django.http import HttpResponseRedirect

def scipycon_quote(string, encoding="utf-8"):
    """Encodes string to encoding before quoting.
    """
    return urllib.quote(string.encode(encoding))

# from LFS
def set_message_cookie(url, msg):
    """Creates response object with given url and adds message cookie with passed
    message.
    """

    # We just keep the message two seconds.
    max_age = 2
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() +
        datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")

    response = HttpResponseRedirect(url)
    response.set_cookie("message", scipycon_quote(msg), max_age=max_age, expires=expires)

    return response

# from django-snippets
def slugify(inStr):
    removelist = ["a", "an", "as", "at", "before", "but", "by", "for","from","is", "in", "into", "like", "of", "off", "on", "onto","per","since", "than", "the", "this", "that", "to", "up", "via","with"];
    for a in removelist:
        aslug = re.sub(r'\b'+a+r'\b','',inStr)
    aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
    aslug = re.sub('\s+', '-', aslug)
    return len(aslug) > 50 and '%s-%d' % (aslug[:43], randint(100000,999999)) or aslug
