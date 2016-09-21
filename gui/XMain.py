from PyQt4.QtGui import *
from PyQt4.QtCore import *

_objs = []
def keep_ref(obj):
    _objs.append(obj)
    return obj

class XMain(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)

        self.buttonNewPlot = QPushButton("New plot")
        self.buttonSavePlot = QPushButton("Save plot")

        self.layout0 = QHBoxLayout()
        self.layout0.addWidget(self.buttonNewPlot)
        self.layout0.addWidget(self.buttonSavePlot)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout0)

        self.setCentralWidget(self.centralWidget)


#         # self.menubar = QMenuBar(self)
#         # self.menubar.setGeometry(QRect(0, 0, 772, 18))
#         #self.menubar.setObjectName(_fromUtf8("menubar"))
#         b = self.menuBar()
#         m = self.menu_file = b.addMenu("&File")
#         self.act_save = ac = m.addAction("&Save")
#         ac.setShortcut("Ctrl+S")
#         ac.triggered.connect(self.on_save)
#         self.act_save_as = ac = m.addAction("Save &as...")
#         ac.setShortcut("Ctrl+Shift+S")
#         ac.triggered.connect(self.on_save_as)
#         m.addSeparator()
#         ac = m.addAction("&Quit")
#         ac.setShortcut("Ctrl+Q")
#         ac.triggered.connect(self.close)
#
#         # * # * # * # * # * # * # *
#         # Final adjustments
#
# #        place_left_top(self)

