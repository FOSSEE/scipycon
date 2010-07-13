# -*- coding: utf-8 -*-
from __future__ import absolute_import

#python imports
import os

#django
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

#django.contrib
from django.contrib.auth.models import User

#PIL
from PIL import Image


def scipycon_createregistrant(request, data):
    """Create user"""
    email = data.get("email")
    name = data.get("name")
    username = data.get("username")

    n = name.split(" ")
    if len(n) > 1:
        first_name = ' '.join(n[:-1])
        last_name = n[-1]
    else:
        first_name = ''
        last_name = n[0]


    # Create user
    user = User.objects.create_user(username=username, email=email)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return user

def scipycon_createuser(request, data):
    """Create user"""
    email = data.get("email")
    username = data.get("username")
    password = data.get("password_1")
    password = data.get("password_1")

    # Create user
    user = User.objects.create_user(
        username=username, email=email, password=password)
    user.first_name = data.get("first_name")
    user.last_name = data.get("last_name")
    user.save()

    # Log in user
    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)

    from django.contrib.auth import login
    login(request, user)

    profile = user.get_profile()
    photo = request.FILES.get('photo', None)
    filename= None
    if photo:
        filename = handle_uploaded_photo(user, request.FILES['photo'])
    if filename:
        profile.photo = filename
    #print photo, filename

    profile.url = data.get("url")
    profile.about = data.get("about")
    profile.save()

    return user

def handle_uploaded_photo(user, ufile):
    usermedia = settings.USER_MEDIA_ROOT
    filename = ufile.name
    ext = filename.split('.')[-1]
    filesize = ufile.size
    filecontent = ufile.read()
    userfilename = 'user-%d.%s' % (user.id, ext)
    if not filecontent:
        return None

    #save
    foutname = os.path.join(usermedia, userfilename)

    fout = file(foutname, 'wb')
    fout.write(filecontent)
    fout.close()

    # crop and resize
    image = Image.open(foutname)
    pw = image.size[0]
    ph = image.size[1]
    nw = nh = 80
    if (pw, ph) != (nw, nh):
        pr = float(pw) / float(ph)
        nr = float(nw) / float(nh)

        if pr > nr:
            # photo aspect is wider than destination ratio
            tw = int(round(nh * pr))
            image = image.resize((tw, nh), Image.ANTIALIAS)
            l = int(round(( tw - nw ) / 2.0))
            image = image.crop((l, 0, l + nw, nh))
        elif pr < nr:
            # photo aspect is taller than destination ratio
            th = int(round(nw / pr))
            image = image.resize((nw, th), Image.ANTIALIAS)
            t = int(round(( th - nh ) / 2.0))
            #print((0, t, nw, t + nh))
            image = image.crop((0, t, nw, t + nh))
        else:
            # photo aspect matches the destination ratio
            image = image.resize((nw, nh), Image.ANTIALIAS)

        image.save(str(foutname))
    return userfilename

