from flask import Flask,request,render_template,redirect,flash,session,g
from dataclasses import dataclass
import base64
import face_recognition
import pickle
from flask.helpers import url_for
from flask_pymongo import PyMongo
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

app=Flask(__name__,template_folder="templates",static_url_path="/")
#连接mongodb,为app设置的内容
#facedata
app.config["MONGO_DBNAME"]="myface_test"
app.config["MONGO_URI"]="mongodb://localhost:27017/myface_test"
#bookdata
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["myface_test"]
mycol = mydb["bookdata"]
#将app应用与mongodb产生联系,使用PyMongo(app)
mongo=PyMongo(app)
flag = 0
username='NULL'
email='NULL'
app.config['SECRET_KEY'] = "sdfklas0lk42jk213khl"
@dataclass
class User:
    id: int
    username: str
faces=mongo.db.myface.find()
users=[]
i=0
for fa in faces:
    i+=1
    users.append(User(i,fa['username']))
# print(users)
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [u for u in users if u.id == session['user_id']][0]
        g.user = user
@app.route("/login",methods=["POST","GET"])
def login():
    msg={}
    if request.method == 'POST':
        # 登录操作
        imgdata=request.form.get("myimg")
        # print(imgdata)
        imgdata=base64.b64decode(imgdata)
        # print(type(imgdata))
        with open("a.png","wb") as f:
            f.write(imgdata)
        faceimg=face_recognition.load_image_file("a.png")
        facedata=face_recognition.face_encodings(faceimg)
        faces=mongo.db.myface.find()
        if facedata!=[]:
            binary_data = pickle.dumps(facedata[0],protocol=-1)
            for fa in faces:
                #取出的数据是myface数据库中的每一条记录face的"face"键对应的值
                facedata_orign=pickle.loads(fa["face"])
                res=face_recognition.compare_faces([facedata[0]],facedata_orign,0.5)
                if res[0] == True:
                    session.pop('user_id', None)
                    username=fa["username"]
                    user = [u for u in users if u.username==username]
                    if len(user) > 0:
                        user = user[0]
                    if user :
                        session['user_id'] = user.id
                        print(users)
                        msg={"result":'登陆成功',"username":username}
                        return msg
            msg={"result":"未匹配到该用户-请先注册"}
            # print(msg)
            return msg
            #return {"result":"人脸数据存储成功"}
        else:            
            msg={"result":"请调整姿势未匹配到人脸"}
            # print(msg)
            return msg
    else:      
        return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        username=request.form.get("username")
        email=request.form.get("email")
        # if username=='' or email=='':
        #     return {"result":"请先完善个人信息"}
        # else:
        #     return {"result":"用户名"+username+"  邮箱"+email}
        # print(username)
        # print(email)
        imgdata=request.form.get("myimg")
        #print(imgdata)
        imgdata=base64.b64decode(imgdata)
        with open("a.png","wb") as f:
            f.write(imgdata)
        faceimg=face_recognition.load_image_file("a.png")
        facedata=face_recognition.face_encodings(faceimg)
        faces=mongo.db.myface.find()
        i=0
        if faces.count() == 0:#mongodb为空，插入第一个用户
            if username=='' or email=='':
                return {"result":"请先完善个人信息"}
            binary_data = pickle.dumps(facedata[0],protocol=-1)
            mongo.db.myface.insert_one({'face':binary_data,'username':username,'email':email})
            return {"result":"第一位用户-注册成功-人脸数据存储成功","username":username,"email":email}
        # print(faces)
        if facedata!=[]:
            binary_data = pickle.dumps(facedata[0],protocol=-1)
            for fa in faces:
                #取出的数据是myface数据库中的每一条记录face的"face"键对应的值
                facedata_orign=pickle.loads(fa["face"])
                res=face_recognition.compare_faces([facedata[0]],facedata_orign,0.5)
                # print(i)
                # print(res)
                # i+=1
                # line = db.myface.count()
                if res[0] == True:
                    return {"result":"该用户已存在，请登录"}
                # else:
            if username=='' or email=='':
                return {"result":"请先完善个人信息"}
            mongo.db.myface.insert_one({'face':binary_data,'username':username,'email':email})
            i+=1
            print(i)
            users.append(User(i,username))
            g.users=users
            return {"result":"注册成功-人脸数据存储成功","username":username,"email":email}
            #return {"result":"人脸数据存储成功"}}
        else:
            # print("请调整姿势未匹配到人脸")
            return {"result":"请调整姿势未匹配到人脸"}

    return render_template("register.html")


@app.route("/logout")
def logout():
    # print("退出")
    session.pop("user_id", None)
    g.user=None
    return redirect(url_for('login'))

@app.route("/index",methods=["POST","GET"])
def index():
    if not g.user:
        # print('NotFound')
        return redirect(url_for('login'))
    print('index')  
    return render_template("index.html")


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
@app.route('/notfound',methods = ['POST', 'GET'])
def notfound():
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

if __name__=="__main__":
    app.run(debug=True)