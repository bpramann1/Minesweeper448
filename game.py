import sys
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import *
from board import Board

class Game(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Minesweeper')  #Sets title of main QWidget
        self.setGeometry(300, 300, 250, 150)    #Sets size of window

        self.layout = QVBoxLayout(self) #Implements a vertical blox layout
        self.layout.addWidget(self.getSize())

        self.setLayout(self.layout) #Adds layout to main widget

    okPressed = False
    rows = 2
    cols = 2

    def getSize(self):
        inputWidget = QWidget()
        inputLayout = QGridLayout()
        inputWidget.setLayout(inputLayout)
        self.grid = []
        self.grid.append([])

        self.grid[0].append(QLabel('# of Rows'))
        inputLayout.addWidget(self.grid[0][0], 0, 0)
        self.rowInput = QLineEdit(self)
        self.intValidator = QIntValidator(self)
        self.rowInput.setValidator(self.intValidator)
        self.grid[0].append(self.rowInput)
        inputLayout.addWidget(self.grid[0][1], 0 , 1)

        self.grid.append([])
        self.grid[1].append(QLabel('# of Columns'))
        inputLayout.addWidget(self.grid[1][0], 1, 0)
        self.colInput = QLineEdit(self)
        self.colInput.setValidator(self.intValidator)
        self.grid[1].append(self.colInput)

        inputLayout.addWidget(self.grid[1][1], 1, 1)
        okButton = QPushButton('OK')
        self.grid[1].append(okButton)
        inputLayout.addWidget(self.grid[1][2], 1, 2)
        okButton.clicked.connect(self.gamestart)

        return inputWidget

    def gamestart(self):
        okPressed = True
        rows = int(self.rowInput.text())
        cols = int(self.colInput.text())
        self.layout.addWidget(self.initTimerWidget())   #Executes the initTimerWidget and adds it to the main widget
        self.board = Board(rows, cols)
        self.layout.addWidget(self.board)

    def initTimerWidget(self):  #Initializes a timer widget which has a horizontal box layout and adds a buttona dn label
        timerWidget = QWidget()
        timerLayout = QHBoxLayout()
        timerButton = QPushButton('Start Timer')
        self.timerLabel = QLabel('Time: 00:00')
        timerWidget.setLayout(timerLayout)
        timerLayout.addWidget(timerButton)
        timerLayout.addWidget(self.timerLabel)
        timerButton.clicked.connect(self.startTimer)
        return timerWidget

    def startTimer(self):   #Connected to the start timer button, initializes a QTime to be decreased and makes a timer event that occurs every 1000 ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
        self.time = QTime(0,0,0,0)
        self.timer.start(1000)

    def time(self): #Function that gets called by the 1000ms timer event
        self.time = self.time.addSecs(1)
        self.timerLabel.setText('Time: ' + str(self.time.toString('mm:ss')))
