import sys
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui

ICON_PATH = 'Icons/flag'

class Tile(QPushButton):
    """A tile button on the minesweeper board

    Holds all data about the tile

    Args:
        i (int): The row of the tile
        j (int): The column of the tile
    """
    rightClicked = pyqtSignal()
    def __init__( self, i, j ):

        super().__init__()

        self.flagIcon = QtGui.QIcon(ICON_PATH)
        self.noIcon = QtGui.QIcon()
        self.setIcon(self.noIcon)

        self.setStyleSheet("border: 1px solid black; height: 35px; width: 30px;")
        self.row = i
        self.col = j
        self.count = 0
        self.mine = False
        self.visible = False
        self.flagged = False

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
        """Updates the state of the button. Is called on left click
        Returns:
            None: None
        """
        if not self.visible:
            self.setText("?")
        elif self.mine:
            self.setText( "M" )
            self.setStyleSheet("border: 1px solid black; height: 35px; width: 30px; background-color: red;")
        else:
            self.setText( "%d" % self.count )
        return None

    def isFlipped(self):
        return self.visible

    def flagMine(self):
        if not self.flagged:
            self.setIcon(self.flagIcon)
            self.flagged = True
            if self.isMine():
                return 1;
        else:
            self.setIcon(self.noIcon)
            self.flagged = False
            if self.isMine():
                return -1;
        return 0;



    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightClicked.emit()
        QPushButton.mousePressEvent(self,event)

