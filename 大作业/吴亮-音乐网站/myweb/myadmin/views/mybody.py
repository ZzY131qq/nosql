import json
from datetime import timedelta

from django.http import HttpResponse, response
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from myadmin.models import User, Music, Friend
from myadmin.views.MusicSpider import MusicSpider

def searchfriend(request):
    myuserid = request.session['adminuser']['id']
    usermode = User.objects
    myuser = usermode.filter(id=myuserid)[0]  # 获取自己的用户信息
    dic = myuser.toDict()  # 用户信息返回字典
    try:
        friendname = request.POST["searchfriend"]
        usermode = User.objects
        frienduser = usermode.filter(username = friendname )[0]
        frienduser_username = frienduser.username
        frienduser_lable = frienduser.lable
        friend_id = frienduser.id
        friendmod = Friend.objects
        friend = friendmod.filter(userid=str(myuserid),friendid=str(friend_id))
        if len(friend) > 0:
            friendmsg = 1
        else:
            friendmsg = 0

    except Exception as e:
        print(e)
        frienduser_username = "没有查找到用户信息"
        frienduser_lable = ""
        friend_id = ""
        friendmsg=""

    context = {"friendusername":frienduser_username,"friendid":friend_id,"friendlable":frienduser_lable,"myuser":dic,"friendmsg":friendmsg}
    return render(request,'myadmin/music/mybody.html',context)

def addfriend(request):
    friendid = request.GET['friendid']
    myuserid = request.session['adminuser']['id']
    friend = Friend()
    friend.userid = str(myuserid)
    friend.friendid = friendid
    friend.save()
    return redirect('/myadmin/mybody')

def delfriend(request):
    friendid = request.GET['friendid']
    myuserid = request.session['adminuser']['id']
    friendmod = Friend.objects
    friend = friendmod.filter(userid=str(myuserid), friendid=str(friendid))
    friend.delete()
    return redirect('/myadmin/mybody')

def mybody(request):
    myuserid = request.session['adminuser']['id']
    usermode = User.objects
    myuser = usermode.filter(id=myuserid)[0]       #获取自己的用户信息
    dic = myuser.toDict()  #用户信息返回字典
    myuserid = request.session['adminuser']['id']
    usermode = User.objects
    myuser = usermode.filter(id=myuserid)[0]  # 获取自己的用户信息
    dic = myuser.toDict()  # 用户信息返回字典
    context = {"myuser":dic}

    return render(request,"myadmin/music/mybody.html",context)


def edit(request):
    try:
        myuserid = request.session['adminuser']['id']
        usermode = User.objects
        myuser = usermode.filter(id=myuserid)[0]  # 获取自己的用户信息
        myuser.username = request.POST['username']
        myuser.gender = request.POST['gender']
        myuser.number = request.POST['number']
        myuser.phonenumber = request.POST['phonenumber']
        myuser.email = request.POST['email']
        myuser.school = request.POST['school']
        myuser.lable = request.POST['lable']
        myuser.save()
        request.session['adminuser'] = myuser.toDict()
        return redirect(reverse("myadmin_mybody"))
    except Exception as e:
        print(e)
        myuserid = request.session['adminuser']['id']
        usermode = User.objects
        myuser = usermode.filter(id=myuserid)[0]  # 获取自己的用户信息
        dic = myuser.toDict()  # 用户信息返回字典
        context = {"info":"性别必须勾选或用户名已存在","myuser":dic}
        return render(request,'myadmin/music/mybody.html',context)