import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tile import Tile


class Board(QWidget):
    """Object that contains a widget for the board that the user interacts with

    Contains functions for detecting clicks at a location, setting mine locations and changing the state of a tile

    Args:
        rows (int): Number of rows
        cols (int): Number of columns
        count (int) : Number of Mines
    """
    def __init__( self, rows, cols, count ):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.tiles = []
        self.mineIndices = []
        self.mineCount = count
        self.minesFound = 0
        self.lost = False
        self.active = True
        self.boardLayout = QGridLayout() #Loads a grid layout


        # create the list of rows * cols unique tiles
        for i in range(0, self.rows):
            self.tiles.append( [] )
            for j in range(0, self.cols):
                self.tiles[i].append( Tile(i, j) )
                self.tiles[i][j].clicked.connect( self.leftClickHandler )
                self.tiles[i][j].rightClicked.connect( self.rightClickHandler )
                self.boardLayout.addWidget( self.tiles[i][j], j, i )

        # assign tiles to be mines
        self.setMines( count )

        self.boardLayout.setSpacing(0)
        self.boardLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout( self.boardLayout )

    def getNeighbors( self, row, col ):
        indices = []
        for i in [ row - 1, row, row + 1 ]:
            validRow = not ( i < 0 or i >= self.rows )
            for j in [ col - 1, col, col + 1 ]:
                validCol = not ( j < 0 or j >= self.cols )
                if validRow and validCol:
                    indices.append( (i, j) )
        return indices

    def setMines( self, count ):
        n = 0
        while n < count:
            i = random.randint( 0, self.rows - 1 )
            j = random.randint( 0, self.cols - 1 )
            if not self.tiles[i][j].isMine():
                self.tiles[i][j].setMine()
                self.mineIndices.append( (i, j) )
                print( "Setting mine at: %d, %d" % (i, j) )
                # increment the mine count on neighboring tiles
                for (y, x) in self.getNeighbors( i, j ):
                  self.tiles[y][x].incCount()
                n += 1
        self.minesSet = True

    # returns True if Tile successfully flips, False if Tile is already flipped
    # returns True even if Tile is a mine
    def flip( self, i, j ):
        # reveal tile and set temp to return value, True if flipped False if not
        temp = self.tiles[i][j].flip()

        if not temp:
            return temp
        elif self.tiles[i][j].isMine():
            self.lost = True
            self.active = False
        elif self.tiles[i][j].getCount() == 0:
            for (row, col) in self.getNeighbors( i, j ):
                self.flip( row, col )
        return temp

    def leftClickHandler(self):
        sender = self.sender()
        (i, j) = sender.getIndices()
        print( "Click detected at %d, %d" % (i, j) )
        temp = self.flip( i, j )
        if not temp:
            print( "Unable to flip already visibile tile" )
        if self.tiles[i][j].isMine():
            print( "Mine uncovered" )

    def rightClickHandler(self):
        sender = self.sender()
        (i, j) = sender.getIndices()
        self.minesFound += self.tiles[i][j].flagMine()
        if self.minesFound == self.mineCount:
            self.win()

    def flipAll(self):
        for i in range( 0, self.rows):
            for j in range( 0, self.cols):
                if not self.tiles[i][j].isMine():
                    self.flip(i,j)
    def win(self):
        self.flipAll()
        print('You won')


