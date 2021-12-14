import json

import requests

from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from base64 import b64encode


from lxml import etree


class MusicSpider:
    def __init__(self,kw):
        self.firsturl = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
        self.kw = kw
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36"
        }
        self.e = "010001"
        self.f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.g = "0CoJUm6Qyw8W8jud"
        self.i = "a8YlfKxjlbqct8IK"


    def get_EncKey(self):
        return "15b80cbe4661d9a2f59580a5f550bf38b106c8b404dd957f8b02907ff42aa06bcd0a267dec83b0e1404d3b6cf590ed0bd7c25e51d2f7a05bc37f3bec2d647bbc053a896561842323df006719685dd7191bca9ee319028f73ac125301973980f6d988d69b753845839b64158cfa77a143539203c92ea3f4af05c5840f3d02d062"


    def get_params(self,data):
        first = self.enc_params(data,self.g)
        second = self.enc_params(first, self.i)
        return second


    def to_16(self,data):
        pad = 16 - len(data) % 16
        data += chr(pad) * pad
        return data


    def enc_params(self,data,key):
        iv = '0102030405060708'
        data = self.to_16(data)
        aes = AES.new(key = key.encode('utf-8'), IV=iv.encode('utf-8'), mode =AES.MODE_CBC)
        bs = aes.encrypt(data.encode('utf-8'))
        return str(b64encode(bs),'utf-8')




    def get_music(self):
        h_url = self.firsturl.format(self.kw, headers=self.headers)
        data = {
            "#/404": "",
            "csrf_token": "",
            "hlposttag": "</span>",
            "hlpretag": "<span class=\"s-fc7\">",
            "limit": "30",
            "offset": "0",
            "s": self.kw,
            "total": "true",
            "type": "1"
        }

        response = requests.post(h_url,headers = self.headers,data={
            "params":self.get_params(json.dumps(data)),
            "encSecKey":self.get_EncKey()
        })

        json1 = response.text
        print(json1)
        return json1

    def get_msg(self):
        musicurl = "https://music.163.com/song/media/outer/url?id="
        dic = json.loads(self.get_music())
        songs = dic['result']['songs']
        res = []
        for song in songs:
            dict = {}
            dict['musicname'] = song['name']
            dict['authorname'] = song['ar'][0]['name']
            dict['music_href'] = musicurl+str(song['id'])
            dict['img_href'] = song['al']['picUrl']
            res.append(dict)
        return res


if __name__ == "__main__":
    MusicSpider("薛之谦").get_msg()