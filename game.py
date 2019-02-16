import sys
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from board import Board

class Game(QWidget):
    def __init__(self,rows,cols,count):
        super().__init__()

        self.setWindowTitle('Minesweeper')  #Sets title of main QWidget
        self.setGeometry(300, 300, 250, 150)    #Sets size of window

        self.layout = QVBoxLayout(self) #Implements a vertical blox layout

        self.setLayout(self.layout) #Adds layout to main widget

        self.rows = rows
        self.cols = cols
        self.count = count
        self.startTimer()
        self.layout.addWidget(self.initTimerWidget())   #Executes the initTimerWidget and adds it to the main widget
        self.board = Board(self.rows, self.cols, self.count)
        self.layout.addWidget(self.board)

    def initTimerWidget(self):  #Initializes a timer widget which has a horizontal box layout and adds a buttona dn label
        timerWidget = QWidget()
        timerLayout = QHBoxLayout()
        self.timerLabel = QLabel('Time: 00:00')
        timerWidget.setLayout(timerLayout)
        timerLayout.addWidget(self.timerLabel)
        return timerWidget

    def startTimer(self):   #Connected to the start timer button, initializes a QTime to be decreased and makes a timer event that occurs every 1000 ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
        self.time = QTime(0,0,0,0)
        self.timer.start(1000)

    def time(self): #Function that gets called by the 1000ms timer event
        self.time = self.time.addSecs(1)
        self.timerLabel.setText('Time: ' + str(self.time.toString('mm:ss')))
