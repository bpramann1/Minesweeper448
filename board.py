import sys
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tile import Tile


class Board(QWidget):
    def __init__(self, rows, cols, count):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.tiles = [][]
        self.minesIndices = []
        self.mineCount = count
        self.flagCount = 0
        self.boardLayout = QGridLayout() #Loads a grid layout

        # create the list of rows * cols unique tiles
        for i in range(0, rows):
          self.tiles.append([])
          for j in range(0, cols):
            self.tiles[i].append(Tile())
            self.boardLayout.addWidget(self.tiles[i][j], i, j)
        
        # assign n tiles to be mines
        for n in range(0, count):
          while True:
            i = random.randint(0, rows - 1)
            j = random.randint(0, cols - 1)
            if not self.tiles[i][j].isMine():
              self.tiles[i].setMine()
              self.mineIndices.append((i,j))
              print("Setting mine at: %d, %d" % (i, j)) 
              # increment the mine count on neighboring tiles
              for x in self.getNeighbors(i):
                self.tiles[x].incCount()
              break

        self.setLayout(self.boardLayout)

    def getNeighbors(self, row, col):
      indices = []
      for i in [row - 1, row, row + 1]:
        for j in [col - 1, col, col + 1]:
          validRow = not (i < 0 or i >= self.rows)
          validCol = not (j < 0 or j >= self.cols)
          if validRow and validCol:
            indices.append((i,j))
      return indices
    
