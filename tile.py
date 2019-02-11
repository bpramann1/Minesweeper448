import sys
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Tile(QPushButton):
    def __init__(self):
        super().__init__("")

    def incCount(self):
        return True

    def setMine(self):
        return True
    
    def isMine(self):
        return False
