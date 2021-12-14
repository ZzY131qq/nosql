import json
from datetime import timedelta

from django.http import HttpResponse, response
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from myadmin.models import Music, Contact, Friend, User


def musicplay(request):
    musicid = request.GET['musicid']
    musicmod = Music.objects
    music = musicmod.filter(id = musicid,status=1)[0]

    mod = User.objects
    user_id = request.session['adminuser']['id']
    friendmod = Friend.objects
    friends = friendmod.filter(userid=str(user_id))
    md = User.objects
    friendict = []
    for friend in friends:
        friendusr = md.filter(id=friend.friendid)
        lable = friendusr[0].lable
        if lable == "":
            lable = "该用户暂无个性签名"
        fdict = {"username": friendusr[0].username, "lable": lable}
        friendict.append(fdict)

    context = {'music':music,"friendict":friendict}
    return render(request, 'myadmin/music/music.html',context)


def contact(request):
    if request.method == 'GET':
        return render(request, 'myadmin/music/contact.html')
    else:
        contact = Contact()
        contact.user_id = request.session['adminuser']['id']
        contact.name = request.POST['name']
        contact.contact = request.POST['email']
        contact.suggestion = request.POST['suggestion']
        contact.save()

    return redirect(reverse('myadmin_contact'))