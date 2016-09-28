"""Library to be probably used in the GUI modules"""

__all__ = ["get_icon"]

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os


def get_icon(keyword):
    """
    Transforms a PNG file in a QIcon

    Looks for a file named <keyword>.png in the "art" directory
    """

    filename = os.path.join("art", keyword+".png")
    ret = QIcon(filename)
    return ret