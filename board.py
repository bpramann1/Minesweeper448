import sys
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tile import Tile


class Board(QWidget):
    def __init__(self, rows, cols):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.boardLayout = QGridLayout() #Loads a grid layout
        self.setLayout(self.boardLayout)
        self.initBoard()

    def initBoard(self):    #Initializes a board widget
        self.setStyleSheet(StyleSheet)
        self.boardLayout.setHorizontalSpacing(0)
        self.boardLayout.setVerticalSpacing(0)
        self.board = [] #creates a two-dimensional array for the board to exist in
        for i in range(0,self.cols):
            self.board.append([])
            for j in range(0,self.rows):
                self.board[i].append(QPushButton(""))
                self.boardLayout.addWidget(self.board[i][j],i,j)
