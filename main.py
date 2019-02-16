import sys
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from game import Game
from PyQt5.QtGui import QIntValidator



class MenuWindow(QWidget):
    """Summary line.

    Extended description of function.

    Args:
        rows (int): Description of rows
        cols (int): Description of cols
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Minesweeper')  #Sets title of main QWidget
        self.setGeometry(300, 300, 250, 150)    #Sets size of window

        self.layout = QVBoxLayout(self) #Implements a vertical blox layout
        self.layout.addWidget(self.getSize())
        self.setLayout(self.layout) #Adds layout to main widget


    def gamestart(self,):
        if len(self.rowInput.text()) and len(self.colInput.text()) and len(self.mineInput.text()) > 0 :
            if (int(self.rowInput.text()) and int(self.colInput.text()) > 1) and (int(self.mineInput.text()) < (int(self.rowInput.text())*int(self.colInput.text()))):
                self.game = Game(int(self.rowInput.text()),int(self.colInput.text()),int(self.mineInput.text()))
                self.game.show()
                self.close()


    def getSize(self):
        inputWidget = QWidget()
        inputLayout = QGridLayout()
        inputWidget.setLayout(inputLayout)

        inputLayout.addWidget(QLabel('# of Rows'), 0, 0)
        self.rowInput = QLineEdit(self)
        self.intValidator = QIntValidator(self)
        self.rowInput.setValidator(self.intValidator)
        inputLayout.addWidget(self.rowInput, 0 , 1)

        inputLayout.addWidget(QLabel('# of Columns'), 1, 0)
        self.colInput = QLineEdit(self)
        self.colInput.setValidator(self.intValidator)
        inputLayout.addWidget(self.colInput, 1, 1)

        inputLayout.addWidget(QLabel('# of Mines'), 2, 0)
        self.mineInput = QLineEdit(self)
        self.mineInput.setValidator(self.intValidator)
        inputLayout.addWidget(self.mineInput, 2, 1)

        self.okButton = QPushButton('OK')
        inputLayout.addWidget(self.okButton, 2, 3)
        self.okButton.clicked.connect(self.gamestart)

        return inputWidget

def main():
    app = QApplication(sys.argv)    #Creates the QT application
    menu = MenuWindow() #Initializes the main widget
    menu.show() #Displays the main widget
    sys.exit(app.exec_()) #Tells the app to run the main loop

main()
