from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIntValidator

class NameInputWindow(QDialog):
    """Object that contains a widget that allows the user to a name
        to be associated with the new high score"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle('New High Score')   #Sets title of main QWidget
        self.setGeometry(300, 300, 250, 150)    #Sets size of window

        self.congratsLabel  = QLabel(self)
        self.nameLabel      = QLabel(self)

        self.congratsLabel.setText("Congratulations!")
        self.nameLabel.setText("Enter your name: ")

        self.congratsLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setAlignment(Qt.AlignCenter)

        self.textbox = QLineEdit(self)
        self.okButton = QPushButton("Continue")
        self.okButton.clicked.connect(self.okButtonCallback)
        self.name = ''

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.congratsLabel)
        self.vbox.addStretch()
        self.vbox.addWidget(self.nameLabel)
        self.vbox.addStretch()
        self.vbox.addWidget(self.textbox)
        self.vbox.addStretch()
        self.vbox.addWidget(self.okButton)
        self.vbox.addStretch()

        self.setLayout(self.vbox)

    """a callback for self.okButton, Used to read the name entered into 
        self.textbox. It also converts all spaces in the name to underscores
        to make parsing easier"""

    def okButtonCallback(self):
        self.name = self.textbox.text()
        self.name = self.name.replace(' ', '_')

        if len(self.name) == 0:
            self.name = "Unknown"

        self.hide()