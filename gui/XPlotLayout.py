<<<<<<< HEAD
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class XPlotLayout(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)



app = QApplication([])
form = MyWindow()
form.show()
app.exec_()

=======
__all__ = ["XPlotLayout"]

class XPlotLayout:
    pass
>>>>>>> f55a0659a4ad6452f07dec36d4e6593f6d4606db
