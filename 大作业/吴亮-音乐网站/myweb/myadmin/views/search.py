import json
from datetime import timedelta

from django.http import HttpResponse, response
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from myadmin.models import User, Music
from myadmin.views.MusicSpider import MusicSpider


def search(request):
    searchvalue = request.GET['searchvalue']
    if searchvalue == "":
        return redirect(reverse("myadmin_main"))
    else:
        musicpy = MusicSpider(searchvalue)
        res = musicpy.get_msg()
        context = {'msgs': res, "key": searchvalue}
    return render(request, 'myadmin/music/search.html', context)


def ilike(request):
    str = request.GET['msg']
    key = request.GET['key']
    msg = eval(str)
    musicmode = Music.objects
    mod = User.objects
    user_id = request.session['adminuser']['id']
    user = mod.filter(id=user_id)
    if len(musicmode.filter(music_href=msg['music_href'], user=user[0],status=1)) > 0:
        return redirect('/myadmin/search?status=0&searchvalue=' + key)
    music = Music()
    music.status = 1
    music.click = 1
    music.musicname = msg['musicname']
    music.authorname = msg['authorname']
    music.music_href = msg['music_href']
    music.img_href = msg['img_href']
    music.user = user[0]
    music.save()
    # music.save()
    context = {'msgs': msg}
    return redirect('/myadmin/search?status=1&searchvalue=' + key)
