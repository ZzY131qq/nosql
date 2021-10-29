import sys

import pymongo
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QAction


class Ui_Form(QMainWindow):
    def setupUi(self, Form):
        #创建菜单栏
        super(Ui_Form, self).__init__(None)
        self.layout = QHBoxLayout()
        self.menubar = self.menuBar()  # 获取窗体的菜单栏
        self.file = self.menubar.addMenu("file")
        self.file.addAction("New File")
        self.save = QAction("Save", self)
        self.save.setShortcut("Ctrl+S")  # 设置快捷键
        self.file.addAction(self.save)
        self.edit = self.file.addMenu("Edit")
        self.edit.addAction("copy")  # Edit下这是copy子项
        self.edit.addAction("paste")  # Edit下设置paste子项
        self.quit = QAction("Quit", self)  # 注意如果改为：self.file.addMenu("Quit") 则表示该菜单下必须柚子菜单项；会有>箭头
        self.file.addAction(self.quit)
        self.file.triggered[QAction].connect(self.processtrigger)
        self.setLayout(self.layout)
        self.setWindowTitle("Menu Demo")

# -- - - - -初始化常量 ----------------------------------------
        self.ischeck = False
        self.conn = None


#一、定义初始化控件---------------------------------------------------------------------------------------------------------
        Form.setObjectName("Form")
        Form.resize(1200, 900)

        # 检查链接按键
        self.check = QtWidgets.QPushButton(Form)
        self.check.setGeometry(QtCore.QRect(20, 590, 115, 31))
        self.check.setStyleSheet("font: 14pt \"华文行楷\";")
        self.check.setObjectName("check")

        #查询全部学生按键
        self.allstudents = QtWidgets.QPushButton(Form)
        self.allstudents.setGeometry(QtCore.QRect(145, 590, 115, 31))
        self.allstudents.setStyleSheet("font: 14pt \"华文行楷\";")
        self.allstudents.setObjectName("allstudents")

        #导出数据按键
        self.out = QtWidgets.QPushButton(Form)
        self.out.setGeometry(QtCore.QRect(270, 590, 150, 31))
        self.out.setStyleSheet("font: 14pt \"华文行楷\";")
        self.out.setObjectName("out")

        #条件查找输入框
        self.tiaojian = QtWidgets.QLineEdit(Form)
        self.tiaojian.setGeometry(QtCore.QRect(440, 590, 165, 31))
        self.tiaojian.setObjectName("tiaojian")

        # 条件查找按键
        self.tiaojianfind = QtWidgets.QPushButton(Form)
        self.tiaojianfind.setGeometry(QtCore.QRect(625, 590, 165, 31))
        self.tiaojianfind.setStyleSheet("font: 14pt \"华文行楷\";")
        self.tiaojianfind.setObjectName("tiaojianfind")

        # 删除按键
        self.dell = QtWidgets.QPushButton(Form)
        self.dell.setGeometry(QtCore.QRect(625, 625, 165, 31))
        self.dell.setStyleSheet("font: 14pt \"华文行楷\";")
        self.dell.setObjectName("dell")

        # 清空按键
        self.clear = QtWidgets.QPushButton(Form)
        self.clear.setGeometry(QtCore.QRect(440, 625, 165, 31))
        self.clear.setStyleSheet("font: 14pt \"华文行楷\";")
        self.clear.setObjectName("clear")
        #主显示界面
        self.photo_lbl = QtWidgets.QLabel(Form)
        self.photo_lbl.setGeometry(QtCore.QRect(20, 60, 850, 510))
        self.photo_lbl.setFrameShape(QtWidgets.QFrame.Box)
        self.photo_lbl.setText("")
        self.photo_lbl.setObjectName("photo_lbl")

        self.lie1 = QtWidgets.QLabel(Form)
        self.lie1.setGeometry(QtCore.QRect(20, 60, 140, 40))
        self.lie1.setFrameShape(QtWidgets.QFrame.Box)
        self.lie1.setText("姓名")
        self.lie1.setObjectName("lie1")

        self.lie2 = QtWidgets.QLabel(Form)
        self.lie2.setGeometry(QtCore.QRect(160, 60, 155, 40))
        self.lie2.setFrameShape(QtWidgets.QFrame.Box)
        self.lie2.setText("学号")
        self.lie2.setObjectName("lie2")

        self.lie3 = QtWidgets.QLabel(Form)
        self.lie3.setGeometry(QtCore.QRect(315, 60, 125, 40))
        self.lie3.setFrameShape(QtWidgets.QFrame.Box)
        self.lie3.setText("年龄")
        self.lie3.setObjectName("lie3")

        self.lie4 = QtWidgets.QLabel(Form)
        self.lie4.setGeometry(QtCore.QRect(440, 60, 150, 40))
        self.lie4.setFrameShape(QtWidgets.QFrame.Box)
        self.lie4.setText("班级")
        self.lie4.setObjectName("lie4")

        self.lie5 = QtWidgets.QLabel(Form)
        self.lie5.setGeometry(QtCore.QRect(590, 60, 140, 40))
        self.lie5.setFrameShape(QtWidgets.QFrame.Box)
        self.lie5.setText("性别")
        self.lie5.setObjectName("lie5")

        self.lie6 = QtWidgets.QLabel(Form)
        self.lie6.setGeometry(QtCore.QRect(730, 60, 140, 40))
        self.lie6.setFrameShape(QtWidgets.QFrame.Box)
        self.lie6.setText("籍贯")
        self.lie6.setObjectName("lie6")

        self.lie11 = QtWidgets.QLabel(Form)
        self.lie11.setGeometry(QtCore.QRect(20, 100, 140, 470))
        self.lie11.setStyleSheet("QLabel{;font-size:30px;font-weight:normal;font-family:Arial;}")
        self.lie11.setFrameShape(QtWidgets.QFrame.Box)
        self.lie11.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lie11.setText("null")
        self.lie11.setObjectName("lie11")

        self.lie21 = QtWidgets.QLabel(Form)
        self.lie21.setGeometry(QtCore.QRect(160, 100, 155, 470))
        self.lie21.setStyleSheet("QLabel{;font-size:30px;font-weight:normal;font-family:Arial;}")
        self.lie21.setFrameShape(QtWidgets.QFrame.Box)
        self.lie21.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lie21.setText("null")
        self.lie21.setObjectName("lie21")

        self.lie31 = QtWidgets.QLabel(Form)
        self.lie31.setGeometry(QtCore.QRect(315, 100, 125, 470))
        self.lie31.setStyleSheet("QLabel{;font-size:30px;font-weight:normal;font-family:Arial;}")
        self.lie31.setFrameShape(QtWidgets.QFrame.Box)
        self.lie31.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lie31.setText("null")
        self.lie31.setObjectName("lie31")

        self.lie41 = QtWidgets.QLabel(Form)
        self.lie41.setGeometry(QtCore.QRect(440, 100, 150, 470))
        self.lie41.setStyleSheet("QLabel{;font-size:30px;font-weight:normal;font-family:Arial;}")
        self.lie41.setFrameShape(QtWidgets.QFrame.Box)
        self.lie41.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lie41.setText("null")
        self.lie41.setObjectName("lie41")

        self.lie51 = QtWidgets.QLabel(Form)
        self.lie51.setGeometry(QtCore.QRect(590, 100, 140, 470))
        self.lie51.setStyleSheet("QLabel{;font-size:30px;font-weight:normal;font-family:Arial;}")
        self.lie51.setFrameShape(QtWidgets.QFrame.Box)
        self.lie51.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lie51.setText("null")
        self.lie51.setObjectName("lie51")

        self.lie61 = QtWidgets.QLabel(Form)
        self.lie61.setGeometry(QtCore.QRect(730, 100, 140, 470))
        self.lie61.setStyleSheet("QLabel{;font-size:30px;font-weight:normal;font-family:Arial;}")
        self.lie61.setFrameShape(QtWidgets.QFrame.Box)
        self.lie61.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lie61.setText("null")
        self.lie61.setObjectName("lie61")

        #log显示框
        self.name = QtWidgets.QTextEdit(Form)
        self.name.setGeometry(QtCore.QRect(10, 670, 860, 210))
        self.name.setObjectName("name")
        self.retranslateUi(Form)

        #右侧，添加学生------------------------------------------------------------------------------------------------------------------------
        #姓名
        self.sname1 = QtWidgets.QLabel(Form)
        self.sname1.setGeometry(QtCore.QRect(880, 60, 80, 40))
        self.sname1.setFrameShape(QtWidgets.QFrame.Box)
        self.sname1.setObjectName("sname1")
        self.sname1.setText("姓名")
        self.sname = QtWidgets.QLineEdit(Form)
        self.sname.setGeometry(QtCore.QRect(970, 60, 200, 40))
        self.sname.setObjectName("sname")
        #学号
        self.sno1 = QtWidgets.QLabel(Form)
        self.sno1.setGeometry(QtCore.QRect(880, 120, 80, 40))
        self.sno1.setFrameShape(QtWidgets.QFrame.Box)
        self.sno1.setObjectName("sno1")
        self.sno1.setText("学号")
        self.sno = QtWidgets.QLineEdit(Form)
        self.sno.setGeometry(QtCore.QRect(970, 120, 200, 40))
        self.sno.setObjectName("sno")
        #年龄
        self.sage1 = QtWidgets.QLabel(Form)
        self.sage1.setGeometry(QtCore.QRect(880, 180, 80, 40))
        self.sage1.setFrameShape(QtWidgets.QFrame.Box)
        self.sage1.setObjectName("sage1")
        self.sage1.setText("年龄")
        self.sage = QtWidgets.QLineEdit(Form)
        self.sage.setGeometry(QtCore.QRect(970, 180, 200, 40))
        self.sage.setObjectName("sage")
        #班级
        self.sgrade1 = QtWidgets.QLabel(Form)
        self.sgrade1.setGeometry(QtCore.QRect(880, 240, 80, 40))
        self.sgrade1.setFrameShape(QtWidgets.QFrame.Box)
        self.sgrade1.setObjectName("sgrade1")
        self.sgrade1.setText("班级")
        self.sgrade = QtWidgets.QLineEdit(Form)
        self.sgrade.setGeometry(QtCore.QRect(970, 240, 200, 40))
        self.sgrade.setObjectName("sgrade")
        #性别
        self.ssex1 = QtWidgets.QLabel(Form)
        self.ssex1.setGeometry(QtCore.QRect(880, 300, 80, 40))
        self.ssex1.setFrameShape(QtWidgets.QFrame.Box)
        self.ssex1.setObjectName("ssex1")
        self.ssex1.setText("性别")
        self.ssex = QtWidgets.QLineEdit(Form)
        self.ssex.setGeometry(QtCore.QRect(970, 300, 200, 40))
        self.ssex.setObjectName("ssex")
        #籍贯
        self.saddress1 = QtWidgets.QLabel(Form)
        self.saddress1.setGeometry(QtCore.QRect(880, 360, 80, 40))
        self.saddress1.setFrameShape(QtWidgets.QFrame.Box)
        self.saddress1.setObjectName("saddress1")
        self.saddress1.setText("籍贯")
        self.saddress = QtWidgets.QLineEdit(Form)
        self.saddress.setGeometry(QtCore.QRect(970, 360, 200, 40))
        self.saddress.setObjectName("saddress")
        #添加按键
        self.adds = QtWidgets.QPushButton(Form)
        self.adds.setGeometry(QtCore.QRect(880, 420, 290, 40))
        self.adds.setStyleSheet("font: 14pt \"华文行楷\";")
        self.adds.setObjectName("adds")
        self.adds.setText("添加学生")
        #右下侧，删除学生--------------------------------------------------------------------------------------------------------------------
        # 姓名
        self.sname11 = QtWidgets.QLabel(Form)
        self.sname11.setGeometry(QtCore.QRect(880, 480, 80, 40))
        self.sname11.setFrameShape(QtWidgets.QFrame.Box)
        self.sname11.setObjectName("sname11")
        self.sname11.setText("姓名")
        self.sname2 = QtWidgets.QLineEdit(Form)
        self.sname2.setGeometry(QtCore.QRect(970, 480, 200, 40))
        self.sname2.setObjectName("sname2")
        # 学号
        self.sno12 = QtWidgets.QLabel(Form)
        self.sno12.setGeometry(QtCore.QRect(880, 540, 80, 40))
        self.sno12.setFrameShape(QtWidgets.QFrame.Box)
        self.sno12.setObjectName("sno12")
        self.sno12.setText("学号")
        self.sno2 = QtWidgets.QLineEdit(Form)
        self.sno2.setGeometry(QtCore.QRect(970, 540, 200, 40))
        self.sno2.setObjectName("sno2")
        # 年龄
        self.sage12 = QtWidgets.QLabel(Form)
        self.sage12.setGeometry(QtCore.QRect(880, 600, 80, 40))
        self.sage12.setFrameShape(QtWidgets.QFrame.Box)
        self.sage12.setObjectName("sage12")
        self.sage12.setText("年龄")
        self.sage2 = QtWidgets.QLineEdit(Form)
        self.sage2.setGeometry(QtCore.QRect(970, 600, 200, 40))
        self.sage2.setObjectName("sage2")
        # 班级
        self.sgrade12 = QtWidgets.QLabel(Form)
        self.sgrade12.setGeometry(QtCore.QRect(880, 660, 80, 40))
        self.sgrade12.setFrameShape(QtWidgets.QFrame.Box)
        self.sgrade12.setObjectName("sgrade12")
        self.sgrade12.setText("班级")
        self.sgrade2 = QtWidgets.QLineEdit(Form)
        self.sgrade2.setGeometry(QtCore.QRect(970, 660, 200, 40))
        self.sgrade2.setObjectName("sgrade2")
        # 性别
        self.ssex12 = QtWidgets.QLabel(Form)
        self.ssex12.setGeometry(QtCore.QRect(880, 720, 80, 40))
        self.ssex12.setFrameShape(QtWidgets.QFrame.Box)
        self.ssex12.setObjectName("ssex12")
        self.ssex12.setText("性别")
        self.ssex2 = QtWidgets.QLineEdit(Form)
        self.ssex2.setGeometry(QtCore.QRect(970, 720, 200, 40))
        self.ssex2.setObjectName("ssex2")
        # 籍贯
        self.saddress12 = QtWidgets.QLabel(Form)
        self.saddress12.setGeometry(QtCore.QRect(880, 780, 80, 40))
        self.saddress12.setFrameShape(QtWidgets.QFrame.Box)
        self.saddress12.setObjectName("saddress12")
        self.saddress12.setText("籍贯")
        self.saddress2 = QtWidgets.QLineEdit(Form)
        self.saddress2.setGeometry(QtCore.QRect(970, 780, 200, 40))
        self.saddress2.setObjectName("saddress2")
        # 修改按键
        self.changes = QtWidgets.QPushButton(Form)
        self.changes.setGeometry(QtCore.QRect(1030, 840, 140, 40))
        self.changes.setStyleSheet("font: 14pt \"华文行楷\";")
        self.changes.setObjectName("changes")
        self.changes.setText("修改信息")
        self.searchone = QtWidgets.QPushButton(Form)
        self.searchone.setGeometry(QtCore.QRect(880, 840, 140, 40))
        self.searchone.setStyleSheet("font: 14pt \"华文行楷\";")
        self.searchone.setObjectName("searchone")
        self.searchone.setText("查找学生")

        QtCore.QMetaObject.connectSlotsByName(Form)

    def processtrigger(self, qaction):
        self.name.setText(qaction.text() + " is triggered!")

    def retranslateUi(self, Form):
#设置控件名称和窗口----------------------------------------------------------------------------------------------------------------------
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "大数据-学生信息管理系统"))
        Form.setWindowIcon(QIcon('data/icon.png'))
        self.check.setText(_translate("Form", "检查连接"))
        self.allstudents.setText(_translate("Form", "全部学生"))
        self.out.setText(_translate("Form", "导出数据"))
        self.tiaojianfind.setText(_translate("Form", "条件查找"))
        self.dell.setText(_translate("Form", "删除该学生"))
        self.clear.setText(_translate("Form", "清空全部"))


class mywindow(Ui_Form, QtWidgets.QWidget):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
#定义槽，这里表示按键控件用什么方法，方法为成员函数------------------------------------------------------------------------------------------
        self.allstudents.clicked.connect(self.show_all_students)
        self.check.clicked.connect(self.check_med)
        self.tiaojianfind.clicked.connect(self.show_one_student)
        self.adds.clicked.connect(self.insert_student)
        self.searchone.clicked.connect(self.find_one)
        self.changes.clicked.connect(self.change_one)
        self.dell.clicked.connect(self.dell_one)
        self.clear.clicked.connect(self.clearall)
        self.out.clicked.connect(self.out_txt)

#检测是否能够连接数据库
    def show_all_students(self):
        if self.ischeck:
            # print(self.conn)
            self.lie11.setText("")
            self.lie21.setText("")
            self.lie31.setText("")
            self.lie41.setText("")
            self.lie51.setText("")
            self.lie61.setText("")
            rets = self.mycol.find()
            if rets:
                # print(rets)
                for ret in rets:
                    # print(ret)
                    # print(ret[5])

                    str0 = self.lie11.text() + '\n' + str(ret["sname"])
                    print(str)
                    self.lie11.setText(str0)
                    self.lie11.repaint()

                    str1 = self.lie21.text() + '\n' + str(ret["sno"])
                    self.lie21.setText(str1)
                    self.lie21.repaint()
                    print(str1)

                    str2 = self.lie31.text() + '\n' + str(ret["sage"])
                    self.lie31.setText(str2)
                    self.lie31.repaint()
                    print(str2)

                    str3 = self.lie41.text() + '\n' + str(ret["banji"])
                    self.lie41.setText(str3)
                    self.lie41.repaint()
                    print(str3)

                    str4 = self.lie51.text() + '\n' + str(ret["xingbie"])
                    self.lie51.setText(str4)
                    self.lie51.repaint()
                    print(str4)

                    str5 = self.lie61.text() + '\n' + str(ret["jiguan"])
                    self.lie61.setText(str5)
                    self.lie61.repaint()
                    print(str5)
                self.name.append("查找成功！！")
        else:
            self.name.append("请先链接数据库！！")

    def show_one_student(self):
        if self.ischeck:
            # cursor = self.conn.cursor()
            # sql = "select * from student where sno = " + str(self.tiaojian.text())
            # cursor.execute(sql)
            myquery = { "sno": self.tiaojian.text() }
            ret = self.mycol.find(myquery)
            print(ret)
            if ret:
                str0 = str(ret["sname"])
                print(str0)
                self.lie11.setText(str0)
                self.lie11.repaint()

                str1 = str(ret["sno"])
                self.lie21.setText(str1)
                self.lie21.repaint()
                print(str1)

                str2 = str(ret["sage"])
                self.lie31.setText(str2)
                self.lie31.repaint()
                print(str2)

                str3 = str(ret["banji"])
                self.lie41.setText(str3)
                self.lie41.repaint()
                print(str3)

                str4 = str(ret["xingbie"])
                self.lie51.setText(str4)
                self.lie51.repaint()
                print(str4)

                str5 = str(ret["jiguan"])
                self.lie61.setText(str5)
                self.lie61.repaint()
                print(str5)
                self.name.append("查找成功！！")
            else:
                self.name.append("未找到该学生!!!")
        else:
            self.name.append("请先链接数据库！！")
##在此处修改数据库设置 -------------------------------------------------------------------------------------------------------------------------------
    def check_med(self):
        try:
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            self.ischeck = True
            self.name.setText("链接成功！")
            self.mydb = myclient.students
            self.mycol = self.mydb.student
        except:
            print("链接失败！")

    def insert_student(self):
        sname = self.sname.text()
        sno = self.sno.text()
        sage = self.sage.text()
        banji = self.sgrade.text()
        xingbie = self.ssex.text()
        jiguan = self.saddress.text()
        # cursor = self.conn.cursor()
        # sql = "insert into student(sname,sno,sage,banji,xingbie,jiguan) values(%s,%s,%s,%s,%s,%s);"  # 增
        # cursor.execute(sql, [sname, sno, sage, banji, xingbie, jiguan])
        # self.conn.commit()
        mydict = { "sname": sname, "sno": sno, "sage": sage, "banji": banji, "xingbie": xingbie, "jiguan": jiguan}
        x = self.mycol.insert_one(mydict)
        self.name.append("插入成功！！")

    def find_one(self):
        if self.ischeck:
            # cursor = self.conn.cursor()
            # sql = "select * from student where sno = " + str(self.sno2.text())
            # cursor.execute(sql)
            # ret = cursor.fetchone()
            myquery = { "sno": self.sno2.text() }
            ret = self.mycol.find_one(myquery)
            print(ret)
            if ret:
                str0 = str(ret["sname"])
                print(str0)
                self.sname2.setText(str0)
                self.sname2.repaint()

                str1 = str(ret["sno"])
                self.sno2.setText(str1)
                self.sno2.repaint()
                print(str1)

                str2 = str(ret["sage"])
                self.sage2.setText(str2)
                self.sage2.repaint()
                print(str2)

                str3 = str(ret["banji"])
                self.sgrade2.setText(str3)
                self.sgrade2.repaint()
                print(str3)

                str4 = str(ret["xingbie"])
                self.ssex2.setText(str4)
                self.ssex2.repaint()
                print(str4)

                str5 = str(ret["jiguan"])
                self.saddress2.setText(str5)
                self.saddress2.repaint()
                print(str5)
                self.name.append("查找成功！！")
            else:
                self.name.append("未找到该学生!!!")
        else:
            self.name.append("请先链接数据库！！")

    def change_one(self):
        try:
            # cursor = self.conn.cursor()
            sname = self.sname2.text()
            sno = self.sno2.text()
            sage = self.sage2.text()
            banji = self.sgrade2.text()
            xingbie = self.ssex2.text()
            jiguan = self.saddress2.text()
            # sql = "update student set sname=%s,sage=%s,banji=%s,xingbie=%s,jiguan=%s where sno=%s"
            # cursor.execute(sql, [sname, sage, banji, xingbie, jiguan, sno])
            # self.conn.commit()
            myquery = { "sno": sno }
            newvalues = {"$set":{ "sname": sname, "sage": sage, "banji": banji, "xingbie": xingbie, "jiguan": jiguan}}
            self.mycol.update_one(myquery, newvalues)
            self.name.append("修改成功！！")
        except:
            self.name.append("未能修改成功！！")

    def dell_one(self):
        # cursor = self.conn.cursor()
        # sql = "delete from student where sno=%s;"
        # sno = self.tiaojian.text()
        # cursor.execute(sql, [sno])
        # self.conn.commit()
        myquery = { "sno": self.tiaojian.text() }
        ret = self.mycol.find(myquery)
        if ret:
            self.mycol.delete_one(myquery)
            self.name.append("删除成功！！")
        else:
            self.name.append("删除失败！！")

    def clearall(self):
        self.tiaojian.setText("")
        self.lie11.setText("")
        self.lie21.setText("")
        self.lie31.setText("")
        self.lie41.setText("")
        self.lie51.setText("")
        self.lie61.setText("")
        self.name.setText("")
        self.sname.setText("")
        self.sno.setText("")
        self.sage.setText("")
        self.sgrade.setText("")
        self.ssex.setText("")
        self.saddress.setText("")
        self.sname2.setText("")
        self.sno2.setText("")
        self.sage2.setText("")
        self.sgrade2.setText("")
        self.ssex2.setText("")
        self.saddress2.setText("")

    def out_txt(self):
        if self.ischeck:
            # cursor = self.conn.cursor()
            # sql = "select * from student"
            # cursor.execute(sql)
            # rets = cursor.fetchmany(20)
            rets = self.mycol.find()
            if rets:
                # print(rets)
                for ret in rets:

                    str0 =  str(ret["sname"])


                    str1 = str(ret["sno"])


                    str2 =  str(ret["sage"])


                    str3 = str(ret["banji"])


                    str4 = str(ret["xingbie"])


                    str5 = str(ret["jiguan"])
                    with open('test.txt', 'a', encoding='utf-8') as f:
                        text = '姓名：'+str0 + ' 学号：' + str1 + ' 年龄：' + str2 + ' 班级：' + str3 +' 性别：'+ str4 + ' 籍贯：' + str5 + '\n'
                        f.write(text)
                self.name.append("导出成功！！")
        else:
            self.name.append("请先链接数据库！！")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = mywindow()
    w.show()
    sys.exit(app.exec_())