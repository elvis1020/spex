#!/usr/bin/python

"""SpeX command-line script"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gui.XMain import XMain


app = QApplication([])
form = XMain()
form.show()
app.exec_()

