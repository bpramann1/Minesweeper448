import sys
import random
import math
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
    endGame = pyqtSignal(str)
    """ Communicates between game and board, emits signal on game end """

    def __init__( self, rows, cols, count, parent = None ):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.tiles = []
        self.mineIndices = []
        self.mineCount = count
        self.minesSet = False
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
                self.boardLayout.addWidget( self.tiles[i][j], i, j )


        self.boardLayout.setSpacing(0)
        self.boardLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout( self.boardLayout )

    def getNeighbors( self, row, col ):
        """Returns the 8 cells surrounding the passed cell

        Args:
            row (int): row of cell to find neighbor for
            col (str): column of cell to find neighbor for

        Returns:
            int[]: 8 row/col pairs for 8 cell neighbors

        """
        indices = []
        for i in [ row - 1, row, row + 1 ]:
            validRow = not ( i < 0 or i >= self.rows )
            for j in [ col - 1, col, col + 1 ]:
                validCol = not ( j < 0 or j >= self.cols )
                if validRow and validCol:
                    indices.append( (i, j) )
        return indices

    def setMines(self, startingPoint):
        """Populates board with mines

        Mine placement is not entirely random. Mines make an attempt to be placed at
        random and there is a chance(placementChance) to allow a mine at that
        random position. This chance to block placement value is a decreasing
        quatratic function that will be 1 at the initial click and 0 at 5% of
        the board away from the initial click. This allows for a small working
        area and eliminates the possibility to hit a mine on first click.

        Args:
            (Int[]): row and column of first tile clicked

        """
        spacing = 0.05
        handicapModifier = 0
        n = 0
        print(startingPoint[0])
        while n < self.mineCount:
            i = random.randint( 0, self.rows - 1 )
            j = random.randint( 0, self.cols - 1 )
            placementRandom = random.uniform(0, 1)
            placementChance =  1-(1/spacing)*math.pow(math.sqrt(math.pow(i-startingPoint[0], 2)+math.pow(j-startingPoint[1],2))/(math.sqrt(math.pow(self.rows, 2)+math.pow(self.cols,2))),2)*(1+handicapModifier)
            if not self.tiles[i][j].isMine():
                if placementRandom > placementChance:
                    self.tiles[i][j].setMine()
                    self.mineIndices.append( (i, j) )
                    # increment the mine count on neighboring tiles
                    for (y, x) in self.getNeighbors( i, j ):
                      self.tiles[y][x].incCount()
                    n += 1
                else:
                    handicapModifier += 1/(100*self.mineCount)
        self.minesSet = True

    # returns True if Tile successfully flips, False if Tile is already flipped
    # returns True even if Tile is a mine
    def flip( self, i, j ):
        """Flips tile at passed location

        Checks where the the passed tile can be flipped and if so flip. If no mines 1 block away from indices passed, flip adjacent tiles.

        Args:
            i (int): row of tile to flip
            j (str): col of tile to flip

        Returns:
            bool: True if tile was flipped, false if not able to flip tile

        """
        # reveal tile and set temp to return value, True if flipped False if not
        temp = self.tiles[i][j].flip()

        if not temp:
            return temp
        elif self.tiles[i][j].isMine():
            self.lost = True
            self.active = False
        elif self.tiles[i][j].getCount() == 0:
            for (row, col) in self.getNeighbors( i, j ):
                if not self.tiles[row][col].isFlipped():
                    self.flip( row, col )
        return temp

    def leftClickHandler(self):
        """Run when a tile is left clicked, calls various functions based on gamestate and state of tile

        Attempts to flip the tile clicked on. If it was a mine proceed to lose state and if not call flip.

        """
        sender = self.sender()
        (i, j) = sender.getIndices()
        if not self.minesSet:
            self.setMines((i,j))
        print( "Click detected at %d, %d" % (i, j) )
        if self.tiles[i][j].isFlagged():
            self.minesFound += self.tiles[i][j].flagMine()
        temp = self.flip( i, j )
        if not temp:
            print( "Unable to flip already visibile tile" )
        if self.tiles[i][j].isMine():
            self.lose()

    def rightClickHandler(self):
        """Run with a tile is right clicked, calls various functions based on gamestate and state of tile

        Flag the tile clicked and if only all mines have been flagged proceed to win state

        """
        sender = self.sender()
        (i, j) = sender.getIndices()
        if not (self.tiles[i][j].isFlipped()):
            self.minesFound += self.tiles[i][j].flagMine()
            if self.minesFound == self.mineCount:
                self.win()

    def flipAll(self, won):
        """Flips all tiles on the board

        Args:
            won (bool): true if game is won, false otherwise

        """
        for i in range( 0, self.rows):
            for j in range( 0, self.cols):
                if won:
                    if not self.tiles[i][j].isMine():
                        self.flip(i,j)
                else:
                    self.flip(i,j)


    def cheatFlipAll(self):
        for i in range( 0, self.rows):
            for j in range( 0, self.cols):
                if self.tiles[i][j].isMine():
                    self.tiles[i][j].cheatBombRevealed = True
                    self.tiles[i][j].displayIcon()

    def cheatFlipBack(self):
        for i in range( 0, self.rows):
            for j in range( 0, self.cols):
                if self.tiles[i][j].isMine():
                    self.tiles[i][j].cheatBombRevealed = False
                    self.tiles[i][j].displayIcon()





    def win(self):
        """Called when game is won, flips all tiles and emits endGame signal which is caught in Game class

        """
        self.flipAll(True)
        self.endGame.emit('won')

    def lose(self):
        """Called when game is lost, flips all tiles and emits endGame signal which is caught in Game class

        """
        self.flipAll(False)
        self.endGame.emit('lost')
