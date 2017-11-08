__all__ = ["XMain"]

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from .guimisc import *
import numpy as np
import matplotlib.pyplot as plt


class XMain(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)

        self.setWindowTitle("SpeX toolbar")
        self.setWindowIcon(get_icon("spexicon_barX"))

        # self.buttonNewPlot = QPushButton("New plot", get_icon("new-plot"))
        # self.buttonSavePlot = QPushButton("Save plot")


        # self.layout0.addWidget(self.buttonNewPlot)
        # self.layout0.addWidget(self.buttonSavePlot)


        # # All actions
        self.action_newPlot = QAction(get_icon("new-plot"), "&New Plot", self)
        self.action_savePlot = QAction(get_icon("save-plot"), "&Save Plot", self)
        self.action_openPlot = QAction(get_icon("open-plot"), "&Open Plot", self)
        self.action_help = QAction(get_icon("help"), "&Help Topics...", self)
        self.action_about = QAction(get_icon("help"), "&About", self)


        # # Menu bar
        # Creates menu bar and adds actions to it
        mb = self.menuBar()
        m = keep_ref(mb.addMenu("&File"))
        ac = keep_ref(m.addAction("&Quit"))
        ac.setShortcut("Ctrl+Q")
        ac.triggered.connect(self.close)

        m = keep_ref(mb.addMenu("&Plot"))
        ac = self.action_newPlot #= keep_ref(m.addAction("&New Plot"))
        ac.triggered.connect(self.testplot)
        
        m.addAction(self.action_savePlot)
        m.addAction(self.action_openPlot)

        m = keep_ref(mb.addMenu("&Help"))
        m.addAction(self.action_help)
        m.addAction(self.action_about)

        # # Tool bar
        # Creates tool bar and adds actions to it
        tb = self.toolBar = QToolBar()
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tb.addAction(self.action_newPlot)
        tb.addAction(self.action_savePlot)
        tb.addAction(self.action_openPlot)
        tb.addAction(self.action_help)


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



        # # Main layout
        # Just the tool bar and a spacer below

        self.layout0 = QVBoxLayout()
        self.layout0.addWidget(self.toolBar)
        self.layout0.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout0)


        self.setCentralWidget(self.centralWidget)

    def testplot(self):
        fig1 = plt.figure("test plot")
        ax1 = fig1.add_subplot(111)
        xl = np.linspace(0, 10, 100)
        ax1.plot(xl, np.sin(xl))
        plt.ion()
        plt.show(fig1)
