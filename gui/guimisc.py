"""Library to be probably used in the GUI modules"""

__all__ = ["get_icon", "keep_ref"]

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


_objs = []
def keep_ref(obj):
    """
    Keeps a reference to a Python object

    Use this when you do not want to bother assigning a Qt Widget to a class
     attribute

    This is to prevent Python object from being garbage-collected when
    corresponding C++ object exists
    """
    _objs.append(obj)
    return obj

