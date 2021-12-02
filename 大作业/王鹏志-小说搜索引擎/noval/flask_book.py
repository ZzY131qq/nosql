from re import I
from flask import Flask, redirect, url_for, request,render_template
import pymongo
import re
import jieba
from flask_paginate import Pagination

#搜索匹配字符串
def is_in(sub_str,full_str):
    if re.findall(sub_str, full_str):
        return full_str
    else:
        return False

app = Flask(__name__)

#连接mongo数据库
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["myfirstDB"]
mycol = mydb["bookdata"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_url/<path:bookurl>')
def book_url(bookurl,limit=15):
   # print(bookurl)
   book_list = []
   b = []
   if bookurl[0] != '[':
      b.append(bookurl)
   else:
      b = bookurl[1:-1].split(',')
      # print(b)
      for i in range(0,len(b)):
         if i == 0:
            b[i] = b[i][1:-1]
         else:
            b[i] = b[i][2:-1]
   print(b)
   for u in b:
      myquery = { "book_url": u}
      mydoc = mycol.find(myquery)
      for x in mydoc:
         a = {'书名':'','网址':''}
         a['书名'] = x['book_name']
         a['网址'] = x['book_url']
         # print(x)
         # print(a)
         book_list.append(a)
   # print(book_list)
   data = book_list
   page = int(request.args.get("page", 1))
   start = (page - 1) * limit
   end = page * limit if len(data) > page * limit else len(data)
   total = int(len(data))
   paginate = Pagination(bs_version=3,page=page, total=len(data),outer_window=0, inner_window=1)
   ret = data[start:end]
   
   totalPage = total / limit if total % limit == 0 else (total / limit) + 1
   averagePage = int(totalPage/page) + 1
   pageInfo={"nowPage":page, "pageSize":limit, "total":total, "totalPage":totalPage,"averagePage":averagePage}
   return render_template('found.html',datas=ret,pageInfo=pageInfo, paginate=paginate,bookurl=bookurl)


#接受前端传来的小说名字，并在数据库里面搜索
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      book_names = []
      jieguo_yesandno = 0
      #接受前端发来的小说名字
      book_name = request.form['search']
      #结巴分词处理
      ss = jieba.cut_for_search(book_name) 
      ss = (" ".join(ss))
      ss = ss.split(" ")
      #匹配书名
      for x in mycol.find({},{ "_id": 0, "book_name": 1}):
         for name in ss:
            jieguo = is_in(name,x['book_name'])
            if jieguo == False:
               pass
            else:
               book_names.append(jieguo)
               jieguo_yesandno += 1
      if jieguo_yesandno == 0:
         return render_template('notfound.html')
      else:
         url = []
         for book in book_names:
            myquery = {'book_name':book}
            mydoc = mycol.find(myquery)
            for x in mydoc:
               url.append(x['book_url'])
         return redirect(url_for('book_url',bookurl = url))
      # #获取对应url值
      # myquery = {'book_name':{ "$regex": "^{}".format(book_name)}}
      # mydoc = mycol.find(myquery)
      # url = []
      # for x in mydoc:
      #    url.append(x['book_url'])
      # if url:
      #    return redirect(url_for('book_url',bookurl = url))
      # else:
      #    return render_template('notfound.html')


   elif request.method == 'GET':
      #接受前端发来的小说名字
      book_name = request.args.get('search')
      #获取对应url值
      myquery = {'book_name':{ "$regex": "^{}".format(book_name)}}
      mydoc = mycol.find(myquery)
      url = []
      for x in mydoc:
         url.append(x['book_url'])
      if url:
         return redirect(url_for('book_url',bookurl = url))
      else:
         return render_template('notfound.html')

   # else:
   #    return render_template('notfound.html')

if __name__ == '__main__':
   app.run(debug = True)