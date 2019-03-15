import sys
import os
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from board import Board

class Game(QWidget):
    """The Game window that is opened on submission of menuWindow

    Contains a board widget and a timer widget

    Args:
        rows (int): Number of rows for the board
        cols (int): Number of columns for the board
        count (int): Number of mines for the board
    """
    def __init__(self, rows ,cols, count):
        super().__init__()

        self.setWindowTitle('Minesweeper')  #Sets title of main QWidget
        self.setGeometry(300, 300, 250, 150)    #Sets size of window
        self.setStyleSheet(StyleSheet)
        self.layout = QVBoxLayout(self) #Implements a vertical blox layout

        self.setLayout(self.layout) #Adds layout to main widget

        self.rows = rows
        self.cols = cols
        self.count = count
        self.startTimer()
        self.layout.addWidget(self.initTimerWidget())   #Executes the initTimerWidget and adds it to the main widget
        self.board = Board(self.rows, self.cols, self.count, self)
        self.board.endGame.connect(self.showEndGameButtons)
        self.layout.addWidget(self.board)

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            print('key pressed: %i' % event.key())
            if event.key() == 66:#66 is the key b
                if not self.board.minesSet:
                    self.board.setMines((-1,-1))
                self.board.cheatFlipAll()

    def initTimerWidget(self):  #Initializes a timer widget which has a horizontal box layout and adds a buttona dn label
        """Initializes the widget that contains the timer label and the timer information

        Makes a QLabel to display text and encapsulates it in a widget



        Returns:
            QWidget: The timer widget

        """
        timerWidget = QWidget()
        timerLayout = QHBoxLayout()
        self.timerLabel = QLabel('Time: 00:00')
        timerWidget.setLayout(timerLayout)
        timerLayout.addWidget(self.timerLabel)
        return timerWidget

    def startTimer(self):   #Connected to the start timer button, initializes a QTime to be decreased and makes a timer event that occurs every 1000 ms
        """Makes and starts the timer

        Instantiates a QTimer and a QTime. QTime is the value of the time set and QTimer gets started to call the time function every 1000ms

        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
        self.time = QTime(0,0,0,0)
        self.timer.start(1)

    def time(self): #Function that gets called by the 1ms timer event
        """Increments the timer by 1 millisecond

        Adds 1 millisecond to the QTime and updates the QLabel with the new time

        """
        self.time = self.time.addMSecs(1)
        if QTime.msec(self.time) == 0:
            self.timerLabel.setText('Time: ' + str(self.time.toString('mm:ss')))

    def showEndGameButtons(self, result):
        """Displays the restart button, whether the player won or lost and stops the timer

        Args:
            result (str): win or lose depending on the result of the game

        """
        self.timer.timeout.disconnect()

        if result == 'won':
            self.updateScoreBoard()

        self.board.setEnabled(False)
        self.resultLabel = QLabel('You %s' % result)
        self.restartButton  = QPushButton('Restart')
        self.restartButton.clicked.connect(self.restartGame)
        self.layout.addWidget(self.resultLabel)
        self.layout.addWidget(self.restartButton)

    def restartGame(self):
        """Called when restart button is clicked. Reopens the menu

        Imports the MenuWindow class to open, Instantiates it, and tells the application to show it. Closes game window shortly after.

        """
        from menuWindow import MenuWindow
        self.menu = MenuWindow()
        self.menu.show()
        self.close()

    def calculateScore(self):
        """Uses the number of mines and the time taken to complete the game to calculate the score"""
        timeHour = QTime.hour(self.time)
        print("\r\ntimeHour = ")
        print(timeHour)
        timeMinute = QTime.minute(self.time)
        print("\r\ntimeMinute = ")
        print(timeMinute)
        timeSecond = QTime.second(self.time)
        print("\r\ntimeSecond = ")
        print(timeSecond)
        timeMillisecond = QTime.msec(self.time)
        print("\r\ntimeMillisecond = ")
        print(timeMillisecond)
        timeScore = ( (timeHour * 3600) + (timeMinute * 60) + (timeSecond) + (timeMillisecond/1000) + 2) / 2
        print("\r\ntimeScore = ")
        print(timeScore)
        if ((self.cols * self.rows) - self.count) > 1:
            mineScore = (self.count * self.count) * ((self.cols * self.rows) - self.count) * 500 
        else:
            mineScore = 0
        print("\r\nmineScore = ")
        print(mineScore)
        totalScore = int(mineScore / timeScore)
        print("\r\ntotalScore = ")
        print(totalScore)
        finalScore = str(totalScore).zfill(12)
        return finalScore


    def writeScoreboard(self):
        """Updates the scoreboard with the most recent score
        requires addition of the os library"""
        finalScore = self.calculateScore()
        if os.path.isfile("scoreboard.txt"):
            infile = open("scoreboard.txt", "r")
            filetext = infile.readlines()
            infile.close()
            if len(filetext) < 10:
                outfile = open("scoreboard.txt", "a+")
                outVal=len(filetext)
                output = "\r\n"+str(outVal)+"."+finalScore
                outfile.write(output)
            else:
                placeNumber = 10
                for x in filetext:
                    if int(filetext[x][2:]) < totalScore:
                        placeNumber = x
                        break
                if placeNumber == 9:
                    filetext[placeNumber] = "10."+finalScore
                else:
                    tempVal = filetext[placeNumber][2:]
                    while placeNumber < 9:
                        filetext[placeNumber] = str(placeNumber+1)+"."+finalScore
                        placeNumber += 1
                        finalScore = tempVal
                        tempVal = filetext[placeNumber][2:]
                    fileText[placeNumber] = "10."+finalScore
                outfile = open("scoreboard.txt", "w")
                for x in filetext:
                    outfile.write(filetext[x])
                outfile.close()
        else:
            outfile = open("scoreboard.txt", "w+")
            outfile.write("1.")
            outfile.write(finalScore)
            outfile.close()

    def calculateHighScoreIndex(self):
        """If the current score is a high score returns the placement of the score,
            returns -1 if the score is not a high score"""

        inFile = open("scoreboard.txt", 'r')
        currentScore = float(self.calculateScore())

        scoreNumber = 0

        for line in inFile:
            scoreInFile = float(line)
            scoreNumber += 1

            if scoreInFile < currentScore:
                return scoreNumber


        if scoreNumber < 10:
            return scoreNumber
        else:
            return -1


    def updateScoreBoard(self):
        highScoreIndex = self.calculateHighScoreIndex()

        if highScoreIndex < 0:
            return

        inFile = open("scoreboard.txt", 'r')
        scores = []
        currentScore = self.calculateScore()

        for line in inFile:
            scores.append(float(line))

        inFile.close()
        outFile = open("scoreboard.txt", "w")

        if highScoreIndex > -1:
            if highScoreIndex > len(scores) -1:
                scores.append(float(currentScore))
            else:
                scores[highScoreIndex] = float(currentScore)

        for score in scores:
            outFile.write(str(score))
            outFile.write('\n')
