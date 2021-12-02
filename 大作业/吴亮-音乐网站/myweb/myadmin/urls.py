"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myadmin.views import index, search, music, mybody, friend

urlpatterns = [
    #主页面
    path('', index.login,name='myadmin_login'),
    path('myadmin',index.main,name='myadmin_main'), #主页面
    path("myadmin/delete",index.delete,name = "myadmin_delete"), #歌单删除


    #搜索
    path('myadmin/logout',index.logout,name='myadmin_logout'),
    path('myadmin/search',search.search,name='myadmin_search'),
    path('myadmin/ilike',search.ilike,name='myadmin_ilike'),

    #音乐
    path('myadmin/music',music.musicplay,name = 'myadmin_musicplay'),

    #联系
    path('myadmin/contact',music.contact,name='myadmin_contact'),

    #好友/个人主页
    path('myadmin/searchfriend',mybody.searchfriend,name="myadmin_searchfriend"),
    path('myadmin/addfriend',mybody.addfriend,name="myadmin_addfriend"),
    path('myadmin/delfriend',mybody.delfriend,name="myadmin_delfriend"),
    path('myadmin/mybody',mybody.mybody,name="myadmin_mybody"),
    path('myadmin/edit',mybody.edit,name="myadmin_edit"),

    #好友主页
    path("myadmin/friend/<str:username>",friend.index,name="myadmin_friend"),
    path("myadmin/music/<str:username>",friend.music,name="myadmin_music")
]
