from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from game import Game
from PyQt5.QtGui import QIntValidator

class MenuWindow(QWidget):
    """The original menu that pops up on launch

    Takes input for rows, columns, and number of mines to be on board and opens a board with those values.

    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Minesweeper')  #Sets title of main QWidget
        self.setGeometry(300, 300, 250, 150)    #Sets size of window
        self.setStyleSheet(StyleSheet)
        self.layout = QVBoxLayout(self) #Implements a vertical box layout
        self.layout.addWidget(self.setForm())
        self.setLayout(self.layout) #Adds layout to main widget


    def gamestart(self):
        """Collects user input needed to start game, bound-checks user supplied values

        Is called on click of okButton. Reads the values from the input fields
        and checks to see if they are within bounds. Rows and columns must be
        greater than 2 and number of mines must be less than rows*columns

        """
        # Collect user input, pass it through the integer parser. Raises exceptions on
        # empty string, dimensions less than 2, or a mine count less than 1 or greater than
        # the board's dimensions.
        # Qt's built in validator system for textboxes prevents non-integer input.
        try:
            rowC = int(self.rowInput.text())
            colC = int(self.colInput.text())
            mineC = int(self.mineInput.text())
            if rowC < 2 or colC < 2 or rowC > 30 or colC > 30:
                raise ValueError("INVALID_DIM")
            if mineC < 1 or mineC > rowC * colC - 1:
                raise ValueError("INVALID_MINE")
            self.game = Game(rowC, colC, mineC)
            self.game.show()
            self.close()
        except ValueError as err:
            if err.args[0] == "INVALID_DIM":
                msg = "Row and column dimensions must be larger than 2 and less than 31"
            elif err.args[0] == "INVALID_MINE":
                msg = "Mine count must be between 1 and the product of the number of rows and columns."
            else:
                msg = "Invalid input."
            QMessageBox.about(self, "Invalid Input Detected", msg)

    def setForm(self):
        """Initial setup for fields on menu

        Makes a QLineEdit for rows, columns, and mines. Limits input to only
        integers. Makes a QPushButton for the okButton and hooks it to
        gamestart()

        """
        inputWidget = QWidget()
        inputLayout = QGridLayout()
        inputWidget.setLayout(inputLayout)

        # Prevent users from entering non-integer values into textboxes
        intValidator = QIntValidator(self)

        inputLayout.addWidget(QLabel('# of Rows'), 0, 0)
        self.rowInput = QLineEdit(self)
        self.rowInput.setValidator(intValidator)
        inputLayout.addWidget(self.rowInput, 0 , 1)

        inputLayout.addWidget(QLabel('# of Columns'), 1, 0)
        self.colInput = QLineEdit(self)
        self.colInput.setValidator(intValidator)
        inputLayout.addWidget(self.colInput, 1, 1)

        inputLayout.addWidget(QLabel('# of Mines'), 2, 0)
        self.mineInput = QLineEdit(self)
        self.mineInput.setValidator(intValidator)
        inputLayout.addWidget(self.mineInput, 2, 1)

        self.okButton = QPushButton('OK')
        inputLayout.addWidget(self.okButton, 2, 3)
        self.okButton.clicked.connect(self.gamestart)

        return inputWidget

    def showMenu():
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self) 
        impMenu.addAction(impAct)
        
        newAct = QAction('New', self)        
        
        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Submenu')    
        self.show()
        menubar.show()
        fileMenu.show() 
