from UI2 import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from UI2 import mywindow
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = mywindow()
    w.show()
    sys.exit(app.exec_())