from flask import Flask,request,render_template
import base64
import face_recognition
from bson.binary import Binary
import pickle
from flask_pymongo import PyMongo
from PIL import Image,ImageDraw
import numpy as np
from bson import binary
app=Flask(__name__,template_folder="templates")
#连接mongodb,为app设置的内容
app.config["MONGO_DBNAME"]="myface"
app.config["MONGO_URI"]="mongodb://localhost:27017/myface_test"
#将app应用与mongodb产生联系,使用PyMongo(app)
mongo=PyMongo(app)
flag = 0
@app.route("/register",methods=["POST","GET"])
def hello():
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
        print(faces)
        if facedata!=[]:
            binary_data = pickle.dumps(facedata[0],protocol=-1)
            for fa in faces:
                #取出的数据是myface数据库中的每一条记录face的"face"键对应的值
                facedata_orign=pickle.loads(fa["face"])
                res=face_recognition.compare_faces([facedata[0]],facedata_orign,0.5)
                # print(i)
                print(res)
                # i+=1
                # line = db.myface.count()
                if res[0] == True:
                    return {"result":"该用户已存在"}
                # else:
            if username=='' or email=='':
                return {"result":"请先完善个人信息"}
            mongo.db.myface.insert_one({'face':binary_data,'username':username,'email':email})
            return {"result":"注册成功-人脸数据存储成功","username":username,"email":email}
            #return {"result":"人脸数据存储成功"}
        else:
            print("请调整姿势未匹配到人脸")
            return {"result":"请调整姿势未匹配到人脸"}

    return render_template("register.html")

if __name__=="__main__":
    app.run()