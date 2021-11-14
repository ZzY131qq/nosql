from flask import Flask,request,render_template
import base64
import face_recognition
from bson.binary import Binary
import pickle
from flask_pymongo import PyMongo
from PIL import Image,ImageDraw
import numpy as np
from bson import binary
from pkg_resources import NullProvider
app=Flask(__name__,template_folder="templates")
#连接mongodb,为app设置的内容
app.config["MONGO_DBNAME"]="myface_test"
app.config["MONGO_URI"]="mongodb://localhost:27017/myface_test"
#将app应用与mongodb产生联系,使用PyMongo(app)
mongo=PyMongo(app)
flag = 0
username='NULL'
email='NULL'
@app.route("/login",methods=["POST","GET"])
def hello():
    if request.method == "POST":
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
            return {"result":"您还没有账号请先注册！"}
        print(faces)
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
                    username=fa["username"]
                    email=fa["email"]
                    return {"result":"登陆成功","username":username,"email":email}
                # else:
            #mongo.db.myface.insert_one({'face':binary_data})
            return {"result":"未匹配到该用户-请先注册"}
            #return {"result":"人脸数据存储成功"}
        else:
            print("请调整姿势未匹配到人脸")
            return {"result":"请调整姿势未匹配到人脸"}

    return render_template("login.html")

if __name__=="__main__":
    app.run()