import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui

ICON_PATH = 'Icons/flag'
CHEAT_FLAGGED_ICON_PATH = 'Icons/cheatFlag'
CHEAT_UNFLAGGED_ICON_PATH = 'Icons/cheatUnflag'

class Tile(QPushButton):
    """A tile button on the minesweeper board

    Holds all data about the tile

    Args:
        i (int): The row of the tile
        j (int): The column of the tile
    """
    rightClicked = pyqtSignal()
    """ NEED DESCRIPTION FOR WHAT THIS IS """
    def __init__( self, i, j ):
        super().__init__()





        self.row = i
        self.col = j
        self.count = 0
        self.mine = False
        self.visible = False
        self.flagged = False
        self.cheatBombRevealed = False

    def getIndices( self ):
        """Returns row and col location of the tile

        Returns:
            (RETURN TYPE): row and col of the tile

        """
        return ( self.row, self.col )

    def getCount(self):
        """Returns number of mines in surrounding 8 neighbor tiles

        Returns:
            int: count of near by mines

        """
        return self.count

    def incCount(self):
        """Increments near by mine count by 1

        Returns:
            bool: always True

        """
        self.count += 1
        return True

    def setMine(self):
        """Attempts to place mine on tile.

        Returns:
            bool: false if tile is already a mine, true otherwise

        """
        if self.mine:
            return False
        else:
            self.mine = True
            return True

    def isMine(self):
        """Returns if tile is a mine

        Returns:
            bool: true if tile is a mine, false otherwise

        """
        return self.mine

    def flip(self):
        """Checks whether the tile has already been click and if not call update()

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

        Returns:
            None: None
        """
        if self.flagged:
            self.flagMine()
        if self.mine:
            self.setText( "M" )
            self.setProperty('class', 'revealedMine')
            self.setStyle(self.style()) #Updates tile to use the correct styling

        else:
            g = max(min(1-self.count/4, 0.75), 0)*200
            r = max(min((self.count/4) - 1, 0.75), 0)*200
            b = (200-g-r)
            if self.count > 0:
                self.setText( "%d" % self.count )
            self.setProperty('class', 'revealed')
            self.setStyleSheet(self.styleSheet() + "Tile{color: rgb(%s, %s, %s);}" % (r,g,b))
            self.setStyle(self.style()) #Updates tile to use the correct styling
        return None

    def isFlipped(self):
        """Returns if tile has been flipped

        Returns:
            bool: true if already flipped, false otherwise

        """
        return self.visible

    def flagMine(self):
        """Toggles the flag on the tile.

        Returns:
            Int: The number to increment the number of mines found, 1 if mine flagged, -1 if mine unflagged, 0 if not a mine

        """
        self.flagged = not self.flagged
        self.displayIcon()
        if (self.isMine() and self.flagged) or (not self.flagged and not self.isMine()):
            return 1
        else:
            return -1
        return 0;

    def displayIcon(self):
        """
        Displays an icon based on the tile.flagged and tile.isflipped properties.
        """
        if self.flagged:
            if (self.cheatBombRevealed and self.isMine()):
                self.flagIcon = QtGui.QIcon(CHEAT_FLAGGED_ICON_PATH)
            else:
                self.flagIcon = QtGui.QIcon(ICON_PATH)
            self.setIcon(self.flagIcon)
        else:
            if not self.isFlipped():
                if (self.cheatBombRevealed and self.isMine()):
                    self.noIcon = QtGui.QIcon(CHEAT_UNFLAGGED_ICON_PATH)
                else:
                    self.noIcon = QtGui.QIcon()
                self.setIcon(self.noIcon)
           
        return 0;

    def isFlagged(self):
        """
        Returns the boolean value of the flagged property of the tile object.
        """
        return self.flagged

    def mousePressEvent(self, event):
        """Is called natively by buttons on mouse press.

        Emits a rightClicked signal on right click and calls the normal QPushButton event system
        """
        if event.button() == Qt.RightButton:
            self.rightClicked.emit()
        QPushButton.mousePressEvent(self,event)
