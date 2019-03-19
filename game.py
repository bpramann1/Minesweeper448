import sys
import os
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from board import Board
from nameInputWindow import *
import time

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
        self.inputWindow = NameInputWindow()
        self.cheatButton  = QPushButton('Cheat')
        self.cheatButton.clicked.connect(self.cheatButtonClicked)
        self.layout.addWidget(self.cheatButton)

    def cheatButtonClicked(self):
        """
        Called when the cheat button is pressed. Calls the cheatFlipAll method of the board object.
        """
        if not self.board.minesSet:
            self.board.setMines((-1,-1))
        if self.cheatButton.text() == "Uncheat":
            self.board.cheatFlipBack()              
        else:
            self.board.cheatFlipAll()

    def keyPressEvent(self, event):
        """Called when a key is pressed, shows all mine tiles
        Args:
            event (QtGui.QKeyEvent): Signal that contains the data on the event
        """
        if type(event) == QtGui.QKeyEvent:
            if event.key() == 66:#66 is the key b
                if not self.board.minesSet:
                    self.board.setMines((-1,-1))
                self.board.cheatFlipAll()
            if event.key() == 86:#66 is the key v
                if not self.board.minesSet:
                    self.board.setMines((-1,-1))
                self.board.cheatFlipBack()


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
        self.timer.start(1000)

    def time(self): #Function that gets called by the 1000ms timer event
        """Increments the timer by 1 second

        Adds 1 second to the QTime and updates the QLabel with the new time

        """
        self.time = self.time.addSecs(1)
        self.timerLabel.setText('Time: ' + str(self.time.toString('mm:ss')))

    def showEndGameButtons(self, result):
        """Displays the restart button, whether the player won or lost and stops the timer

        Args:
            result (str): win or lose depending on the result of the game

        """
        self.timer.timeout.disconnect()

        if result == 'won' and self.calculateHighScoreIndex() >= 0:
            self.inputWindow.exec()
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
        timeMinute = QTime.minute(self.time)
        timeSecond = QTime.second(self.time)
        timeScore = ( (timeHour * 3600) + (timeMinute * 60) + (timeSecond) + 2) / 2
        mineScore = self.count * 5000
        totalScore = int(mineScore / timeScore)
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
            listOfWords = line.split()
            scoreInFile = float(listOfWords[2])
            if scoreInFile < currentScore:
                return scoreNumber
            scoreNumber += 1

        if scoreNumber < 10:
            return scoreNumber
        else:
            return -1


    def updateScoreBoard(self):
        """Updates the scoreboard with the most recent score"""
        
        highScoreIndex = self.calculateHighScoreIndex()

        if highScoreIndex < 0:
            return

        inFile = open("scoreboard.txt", 'r')
        scores = []
        names  = []
        currentScore = self.calculateScore()

        for line in inFile:
            listOfWords = line.split()
            scores.append(float(listOfWords[2]))
            names.append(listOfWords[1])

        inFile.close()
        outFile = open("scoreboard.txt", "w")

        
        scores.append(float(currentScore))
        names.append(self.inputWindow.name)



        if highScoreIndex < len(scores) -1:
            for scoreIndex in range(highScoreIndex, len(scores) -1):
                scores[len(scores) - scoreIndex -1] = scores[len(scores) - scoreIndex - 2]
                names[len(scores) - scoreIndex - 1] = names[len(scores) - scoreIndex - 2]

        if highScoreIndex < len(scores):
            scores[highScoreIndex] = float(currentScore)
            names[highScoreIndex] = self.inputWindow.name

        count = 1
        for score in scores:
            outFile.write(str(count) + "\t\t" + names[count -1] + "\t\t" + str(score))
            outFile.write('\n')
            count += 1

