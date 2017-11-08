#!/usr/bin/python

"""SpeX command-line script"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from gui.XMain import XMain


app = QApplication([])
form = XMain()
form.show()
app.exec_()

