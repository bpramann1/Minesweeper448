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
        self.setStyleSheet(StyleSheet)
        self.layout = QVBoxLayout(self) #Implements a vertical box layout
        self.layout.addWidget(self.setForm())
        self.setLayout(self.layout) #Adds layout to main widget


    def gamestart(self):
        """Collects user input needed to start game, bound-checks user supplied values

        (No args or returns, does this need more explination?)

        """
        # Collect user input, pass it through the integer parser. Raises exceptions on
        # empty string, dimensions less than 2, or a mine count less than 1 or greater than
        # the board's dimensions.
        # Qt's built in validator system for textboxes prevents non-integer input.
        try:
            rowC = int(self.rowInput.text())
            colC = int(self.colInput.text())
            mineC = int(self.mineInput.text())
            if rowC < 2 or colC < 2:
                raise ValueError("INVALID_DIM")
            if mineC < 1 or mineC > rowC * colC - 1:
                raise ValueError("INVALID_MINE")
            self.game = Game(rowC, colC, mineC)
            self.game.show()
            self.close()
        except ValueError as err:
            if err.args[0] == "INVALID_DIM":
                msg = "Row and column dimensions must be larger than 2."
            elif err.args[0] == "INVALID_MINE":
                msg = "Mine count must be between 1 and the product of the number of rows and columns."
            else:
                msg = "Invalid input."
            QMessageBox.about(self, "Invalid Input Detected", msg)
     
    def setForm(self):
        """(Not sure about this one, looks like its setting up the board before that screen is loaded maybe?)

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

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
