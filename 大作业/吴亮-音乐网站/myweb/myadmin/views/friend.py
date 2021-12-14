from datetime import timedelta

from django.core.paginator import Paginator
from django.http import HttpResponse, response
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from myadmin.models import User, Music, Friend

def index(request,username):
    try:
        page = request.GET['page']
        if page == None:
            pIndex = 1              #如果没有给页码自动赋值1
        else:
            pIndex = int(page)      #将页码转为int整型
    except:
        pIndex=1
    #用户歌单
    mod = User.objects
    user_id = request.session['adminuser']['id']
    user = mod.filter(id=user_id)
    friend = mod.filter(username=username)
    try:
        friendname = friend[0].username
        friendlable = friend[0].lable
        musicmodel = Music.objects
        umusics = musicmodel.filter(user=friend[0], status=1)
        p = Paginator(umusics, 12)  # 12条数据一页，实例化分页对象
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

        # 热门榜单
        superadmin = mod.filter(username="superadmin")
        hotmusics = musicmodel.filter(user=superadmin[0], status=1)
        hotmusic_res = []
        for hotmusic in hotmusics:
            dic = hotmusic.toDict()
            hotmusic_res.append(dic)

        # 好友展示
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

        context = {"music_res": music_res, "hotmusic_res": hotmusic_res, "pIndex": pIndex,
                   "pagelist": p.page_range, 'pnum_pages': p.num_pages, "friendict": friendict,
                   "friendname": friendname, "friendlable": friendlable}
        print(friendname)
        return render(request, 'myadmin/friend/friend.html', context)
    except:
        return render(request, 'myadmin/friend/friend.html')





def music(request,username):
    #用户歌单
    mod = User.objects
    user_id = request.session['adminuser']['id']
    user = mod.filter(id=user_id)
    friend = mod.filter(username=username)
    friendname = friend[0].username
    friendlable = friend[0].lable

    musicid = request.GET['musicid']
    musicmod = Music.objects
    music = musicmod.filter(id = musicid,status=1)[0]
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

    context = {'music':music,"friendict":friendict,"friendname":friendname,"friendlable":friendlable}
    return render(request, 'myadmin/friend/music.html',context)