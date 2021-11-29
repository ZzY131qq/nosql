import requests
from lxml import etree
import pymongo



class book_data():
    def __init__(self,kw):

        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        }
        self.kw=kw
        self.base_url="https://www.xbiquge.la/xiaoshuodaquan/"


    
    def down_html(self,url):
        try:
            responce=requests.get(url,headers=self.headers)
            content=responce.content.decode("utf-8","ignore")
            # content=responce.content
            # print("="*30)
            return content
        except Exception as e:
            print("error")
            print(e)
            return ""

    def get_data_to_mgdb(self):
        book_list = []
        #连接数据库
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["book_data"]
        mycol = mydb["bookdata"]
        #获取html源码
        content=self.down_html(self.base_url)
        content=etree.HTML(content)
        div = 1
        while 1:
            book_label=content.xpath("//*[@id='main']/div[{}]/h2//text()".format(div))
            # if div>=5:
            #     break
            if book_label:
                li = 1
                while 1:
                    book_data = {'book_name':'','book_url':'','book_lable':''}
                    book_name=content.xpath('//*[@id="main"]/div[{}]/ul/li[{}]/a//text()'.format(div,li))
                    # if li>=10:
                    #     break
                    if book_name:
                        book_url=content.xpath('//*[@id="main"]/div[{}]/ul/li[{}]/a/@href'.format(div,li))
                        book_data['book_name']=book_name[0]
                        book_data['book_url']=book_url[0]
                        book_data['book_lable']=book_label[0][:-4]
                        # 插入数据库
                        try:
                            #字典插入
                            if mycol.insert_one(book_data):
                                print("执行插入成功")
                        except Exception as e:
                            print("执行失败")
                            print(e)
                        book_list.append(book_data)
                        #print(book_data)
                        li = li+1
                    else:
                        break
                div = div+2
            else:
                break
        myclient.close()
        # print(book_list)
        return book_list

a = book_data("伏天氏")
a.get_data_to_mgdb()