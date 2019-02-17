import sys
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
        """Checks whether the tile has already been click and if not call update()

        Args:

        Returns:
            bool: False if already clicked, True if not
        """
        if self.visible:
            return False
        else:
            self.visible = True
            self.update()
            return True

    def update(self):
        """Updates the state of the button. Called if the tile was left clicked for the first time

        Args:

        Returns:
            None: None
        """
        if self.flagged:
            self.flagMine()
        if self.mine:
            self.setText( "M" )
            self.setProperty('class', 'revealed')
            self.setStyle(self.style()) #Updates tile to use the correct styling
        else:
            self.setText( "%d" % self.count )
        return None

    def isFlipped(self):
        return self.visible

    def flagMine(self):
        """Toggles the flag on the tile.

        Args:

        Returns:
            Int: The number to increment the number of mines found, 1 if mine flagged, -1 if mine unflagged, 0 if not a mine

        """

        if not self.flagged:
            if not self.isFlipped():
                self.setIcon(self.flagIcon)
                self.flagged = True
                if self.isMine():
                    return 1
                else:
                    return -1
        else:
            self.setIcon(self.noIcon)
            self.flagged = False
            if self.isMine():
                return -1
            else:
                return 1
        return 0;

    def mousePressEvent(self, event):
        """Is called natively by buttons on mouse press.

        Emits a rightClicked signal on right click and calls the normal QPushButton event system

        Args:

        Returns:

        """
        if event.button() == Qt.RightButton:
            self.rightClicked.emit()
        QPushButton.mousePressEvent(self,event)

