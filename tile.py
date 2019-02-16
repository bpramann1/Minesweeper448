import sys
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Tile(QPushButton):
    """Summary line.

    Extended description of function.

    Args:
        rows (int): Description of rows
        cols (int): Description of columns
    """
    def __init__( self, i, j ):
        super().__init__("?")

        self.setStyleSheet("border: 1px solid black; height: 35px; width: 30px");
        self.row = i
        self.col = j
        self.count = 0
        self.mine = False
        self.visible = False

    def getIndices( self ):
        return ( self.row, self.col )

    def getCount(self):
        return self.count

    def incCount(self):
        self.count += 1
        return True

    def setMine(self):
        if self.mine:
            return False
        else:
            self.mine = True
            return True

    def isMine(self):
        return self.mine

    def flip(self):
        if self.visible:
            return False
        else:
            self.visible = True
            self.update()
            return True

    def update(self):
        if not self.visible:
            self.setText( "?" )
        elif self.mine:
            self.setText( "M" )
        else:
            self.setText( "%d" % self.count )
        return None

    def isFlipped(self):
        return self.visible
