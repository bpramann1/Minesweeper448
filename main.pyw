#!/usr/bin/python3

import sys
from menuWindow import MenuWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



def main():
    app = QApplication(sys.argv)    #Creates the QT application
    menu = MenuWindow()             #Initializes the main widget
    menu.show()                     #Displays the main widget
    sys.exit(app.exec_())           #Tells the app to run the main loop

if __name__ == '__main__':
    main()
