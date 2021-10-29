import pymongo
 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["students"]
mycol = mydb["student"]
mydict = { "sname": "小明", "sno": "19490256", "sage": "20", "banji": "大数据192", "xingbie": "男", "jiguan": "江苏"}
x=mycol.insert_one(mydict)
print(x)