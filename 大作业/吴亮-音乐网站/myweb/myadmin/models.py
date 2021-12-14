# from typing_extensions import Required
# from django.db import models
from django.db import models
import mongoengine
from pymongo.read_preferences import Primary

# # Create your models here.
# class User(models.Model):
#     objects = None
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=64)
#     email = models.EmailField()
#     phonenumber = models.CharField(max_length=16)
#     school = models.CharField(max_length=64)
#     number = models.CharField(max_length=64)
#     gender = models.CharField(max_length=5)
#     status = models.IntegerField()
#     lable = models.CharField(max_length=255,default="")
#     regist_data = models.DateField(auto_now_add=True)

    # def toDict(self):
    #     return {'id': self.id, 'username': self.username, 'password': self.password, 'email': self.password,
    #             'phonenumber': self.phonenumber, 'school': self.school,'lable':self.lable,
    #             'number': self.number, 'gender': self.gender, 'status': self.status, 'regist_data': self.regist_data}
class User(mongoengine.Document):
    # object=None
    username=mongoengine.StringField(max_length=255,unique=True)
    password=mongoengine.StringField(max_length=64)
    email=mongoengine.EmailField()
    phonenumber=mongoengine.StringField(max_length=16)
    school=mongoengine.StringField(max_length=64)
    number=mongoengine.StringField(max_length=64)
    gender=mongoengine.StringField(max_length=5)
    status=mongoengine.IntField()
    lable=mongoengine.StringField(max_length=255,defult="")
    regist_data=mongoengine.DateField(auti_now_add=True)
    def toDict(self):
        return {'id': self.id, 'username': self.username, 'password': self.password, 'email': self.password,
                'phonenumber': self.phonenumber, 'school': self.school,'lable':self.lable,
                'number': self.number, 'gender': self.gender, 'status': self.status, 'regist_data': self.regist_data}    


# class Music(models.Model):
#     objects = None
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey("User",on_delete=models.CASCADE)
#     musicname = models.CharField(max_length=64)
    # authorname = models.CharField(max_length=64)
    # music_href = models.CharField(max_length=255)
    # click = models.IntegerField()
    # img_href = models.CharField(max_length=255)
    # img = models.ImageField()
    # comments = models.TextField()
    # content = models.TextField()
    # status = models.IntegerField()                    #0代表被删除 1代表正常
    # add_data = models.DateField(auto_now_add=True)


    # def toDict(self):
    #     return {'id':self.id,'user': self.user, 'musicname': self.musicname, 'authorname': self.authorname, 'music_href': self.music_href,
    #             'click': self.click, 'img_href': self.img_href,
    #             'img': self.img, 'comments': self.comments, 'content': self.content, 'status': self.status,'add_data':self.add_data}
class Music(mongoengine.Document):
    # object=None
    id=mongoengine.SequenceField(required=True,primary_key=True)
    user=mongoengine.ReferenceField("User",on_delete=models.CASCADE)
    musicname=mongoengine.StringField(max_length=64)
    authorname = mongoengine.StringField(max_length=64)
    music_href = mongoengine.StringField(max_length=255)
    click = mongoengine.IntField()
    img_href = mongoengine.StringField(max_length=255)
    img = mongoengine.ImageField()
    comments = mongoengine.StringField(max_length=400)
    content = mongoengine.StringField(max_length=400)
    status = mongoengine.IntField()                    #0代表被删除 1代表正常
    add_data = mongoengine.DateField(auto_now_add=True)



    def toDict(self):
        return {'id':self.id,'user': self.user, 'musicname': self.musicname, 'authorname': self.authorname, 'music_href': self.music_href,
                'click': self.click, 'img_href': self.img_href,
                'img': self.img, 'comments': self.comments, 'content': self.content, 'status': self.status,'add_data':self.add_data}    


# class Contact(models.Model):
#     user = models.ForeignKey("User", on_delete=models.CASCADE)
#     name = models.CharField(max_length=64)
#     contact = models.CharField(max_length=64)
#     suggestion = models.CharField(max_length=2000)
class Contact(mongoengine.Document):
    user = mongoengine.ReferenceField("User", on_delete=models.CASCADE)
    name = mongoengine.StringField(max_length=64)
    contact = mongoengine.StringField(max_length=64)
    suggestion = mongoengine.StringField(max_length=2000)


class Friend(mongoengine.Document):
    # objects = None
    userid = mongoengine.StringField(max_length=64)
    friendid = mongoengine.StringField(max_length=64)
