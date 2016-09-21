#!/usr/bin/python

"""Show window in monitor"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        
        label = QLabel("Hello world!!!!!!!!")
        
        self.setCentralWidget(label)


app = QApplication([])
form = MyWindow()
form.show()
app.exec_()

