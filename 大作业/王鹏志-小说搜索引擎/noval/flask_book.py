from flask import Flask, redirect, url_for, request,render_template
import pymongo



app = Flask(__name__)

#连接mongo数据库
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["book_data"]
mycol = mydb["bookdata"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_url/<path:bookurl>')
def book_url(bookurl):
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
   return render_template('found.html',datas = book_list)


#接受前端传来的小说名字，并在数据库里面搜索
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      #接受前端发来的小说名字
      book_name = request.form['search']
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