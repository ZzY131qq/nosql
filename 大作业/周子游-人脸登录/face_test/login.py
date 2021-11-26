from flask import Flask,request,render_template,flash
import base64
import face_recognition
from bson.binary import Binary
import pickle
from flask.helpers import url_for
from flask_pymongo import PyMongo
from PIL import Image,ImageDraw
import numpy as np
from bson import binary
from pkg_resources import NullProvider
app=Flask(__name__,template_folder="templates",static_url_path="/")
#连接mongodb,为app设置的内容
app.config["MONGO_DBNAME"]="myface_test"
app.config["MONGO_URI"]="mongodb://localhost:27017/myface_test"
#将app应用与mongodb产生联系,使用PyMongo(app)
mongo=PyMongo(app)
flag = 0
username='NULL'
email='NULL'
app.config['SECRET_KEY'] = "sdfklas0lk42jk213khl"
@app.route("/login",methods=["POST","GET"])
def login():
    
    msg={}
    # return redirect(url_for('index'))
    if request.method == "POST":
        # return redirect(url_for('index'))
        imgdata=request.form.get("myimg")
        # print(imgdata)
        imgdata=base64.b64decode(imgdata)
        print(type(imgdata))
        with open("a.png","wb") as f:
            f.write(imgdata)
        faceimg=face_recognition.load_image_file("a.png")
        facedata=face_recognition.face_encodings(faceimg)
        faces=mongo.db.myface.find()
        if faces.count() == 0:
            msg={"result":"未匹配到该用户-请先注册"}
            # return render_template("login.html",msg=msg)
            return msg
        if facedata!=[]:
            binary_data = pickle.dumps(facedata[0],protocol=-1)
            for fa in faces:
                #取出的数据是myface数据库中的每一条记录face的"face"键对应的值
                facedata_orign=pickle.loads(fa["face"])
                res=face_recognition.compare_faces([facedata[0]],facedata_orign,0.5)
                if res[0] == True:
                    username=fa["username"]
                    email=fa["email"]
                    msg={"result":'登陆成功'}
                    print(msg)
                    #return redirect(url_for('index'))
                    return msg
               
            msg={"result":"未匹配到该用户-请先注册"}
            print(msg)
            return msg
            return render_template("login.html",msg=msg)
            #return {"result":"人脸数据存储成功"}
        else:            
            msg={"result":"请调整姿势未匹配到人脸"}
            print(msg)
            return msg
            return render_template("login.html",msg=msg)
    else:      
        return render_template("login.html")

@app.route("/index",methods=["POST","GET"])
def index():
    print('index')  
    return render_template("index.html")

@app.route("/register",methods=["POST","GET"])
def register():
    # print('index')  
    return render_template("register.html")

if __name__=="__main__":
    app.run(debug=True)