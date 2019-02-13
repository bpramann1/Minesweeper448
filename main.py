#!/usr/bin/python3

import sys
from Styles import StyleSheet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from game import Game

def main():
    app = QApplication(sys.argv)    #Creates the QT application
    menu = Game() #Initializes the main widget
    menu.show() #Displays the main widget
    app.exec_() #Tells the app to run the main loop

if __name__ == '__main__':
    main()
