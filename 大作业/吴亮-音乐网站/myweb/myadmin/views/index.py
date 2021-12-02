from datetime import timedelta

from django.core.paginator import Paginator
from django.http import HttpResponse, response
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from myadmin.models import User, Music, Friend


def delete(request):
    musicid = request.GET["musicid"]
    musicmod = Music.objects
    mod = User.objects
    user_id = request.session['adminuser']['id']
    music = musicmod.filter(id = musicid,status=1,user_id=user_id)[0]
    music.status = 0
    music.save()
    return redirect(reverse("myadmin_main"))


def main(request):


    try:
        page = request.GET['page']
        if page == None:
            pIndex = 1
        else:
            pIndex = int(page)
    except:
        pIndex=1
    #用户歌单
    mod = User.objects
    user_id = request.session['adminuser']['id']
    user = mod.filter(id=user_id)
    musicmodel = Music.objects
    umusics = musicmodel.filter(user=user[0],status=1)

    p = Paginator(umusics,12)            #12条数据一页，实例化分页对象
    # 判断页码值是否有效
    if pIndex < 1:
        pIndex = 1
    if pIndex > p.num_pages:
        pIndex = p.num_pages
    musics = p.page(pIndex)
    music_res = []
    for music in musics:
        dic = music.toDict()
        music_res.append(dic)


    #热门榜单
    superadmin = mod.filter(username = "superadmin")
    hotmusics = musicmodel.filter(user=superadmin[0],status=1)
    hotmusic_res = []
    for hotmusic in hotmusics:
        dic = hotmusic.toDict()
        hotmusic_res.append(dic)

    #好友展示
    friendmod = Friend.objects
    friends = friendmod.filter(userid=str(user_id))
    md = User.objects
    friendict = []
    for friend in friends:
        friendusr = md.filter(id=friend.friendid)
        lable = friendusr[0].lable
        if lable=="":
            lable = "该用户暂无个性签名"
        fdict = {"username":friendusr[0].username,"lable":lable}
        friendict.append(fdict)


    context = {"music_res":music_res,"hotmusic_res":hotmusic_res,"pIndex":pIndex,"pagelist":p.page_range,'pnum_pages':p.num_pages,"friendict":friendict}
    return render(request, 'myadmin/music/index.html',context)


def login(request):

    if request.method == 'GET':
        context = {"yz":'allow'}
        return render(request, 'myadmin/index/login.html')
    else:
        if request.POST.get("phonenumber") == None:

            model = User.objects



            try:
                model = User.objects

                user = model.get(username=request.POST['username'])
                if user.status == 0:
                    context = {"info": "该账户被禁用"}
                if user.password == request.POST['password']:
                    request.session.set_expiry(timedelta(days=5))

                    request.session['adminuser'] = user.toDict()
                    return redirect(reverse("myadmin_main"))
                else:
                    context = {"info": "用户名或密码错误"}

            except Exception as e:
                print(e)
                context = {"info": "登录账号不存在"}
            return render(request, 'myadmin/index/login.html', context)
        else:
            try:
                user = User()
                user.username = request.POST['username']
                user.password = request.POST['password']
                user.email = request.POST['email']
                user.number = request.POST['number']
                user.phonenumber = request.POST['phonenumber']
                user.school = request.POST['school']
                user.status = 1
                user.save()
                context = {"registinfo": "注册成功"}
            except Exception as e:
                print(e)
                context = {"registinfo": "用户名已存在"}
            return render(request, 'myadmin/index/login.html', context)


def logout(request):
    del request.session['adminuser']
    return redirect(reverse('myadmin_login'))
# # 执行登录
# def dologin(request):
#     try:
#         model = User.objects
#         user = model.get(username=request.POST['username'])
#
#         if user.status == 0:
#             context = {"info": "该账户被禁用"}
#         if user.password == request.POST['password']:
#             request.session.set_expiry(timedelta(days=5))
#             request.session['adminuser'] = user.toDict()
#             return redirect(reverse("myadmin_main"))
#         else:
#             context = {"info": "用户名或密码错误"}
#
#     except Exception as e:
#         print(e)
#         context = {"info": "登录账号不存在"}
#     return render(request, 'myadmin/index/login.html', context)
#
#
# def doregist(request):
#     try:
#         user = User()
#         user.username = request.POST['username']
#         user.password = request.POST['password']
#         user.email = request.POST['email']
#         user.number = request.POST['number']
#         user.phonenumber = request.POST['phonenumber']
#         user.school = request.POST['school']
#         user.status = 1
#         user.save()
#         context = {"registinfo": "注册成功"}
#     except Exception as e:
#         print(e)
#         context = {"registinfo": "用户名已存在"}
#     return render(request, 'myadmin/index/login.html', context)
