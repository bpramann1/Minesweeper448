from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from game import Game
from PyQt5.QtGui import QIntValidator

class HighScoresWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('High Scores')      #Sets title of main QWidget
        self.setGeometry(300, 300, 500, 300)    #Sets size of window

        self.textArea = QPlainTextEdit(self)
        self.textArea.resize(500, 300)
        self.textArea.insertPlainText("Name \t|\t Score")
        self.textArea.insertPlainText('\n')

        inFile = open("scoreboard.txt", 'r')

        for line in inFile:
            self.textArea.insertPlainText(line)


        self.textArea.setReadOnly(True)