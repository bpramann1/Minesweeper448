#!/usr/bin/python3

from Tile import Board

while True:
  dim = (int)(input("Enter dimensions for board: "))
  count = (int)(input("Enter number of mines: "))
  game = Board(dim, count)

  while game.isActive():
    game.render()
    temp = (input("Enter F to flag a mine, S to reveal a space: "))
    if temp == "F":
      guess = (int)(input("Enter the index to flag (between 0 and %d): " % (dim * dim - 1)))
      if not game.flag(guess):
        print("Selected location is already visible or too many flags are used")
    elif temp == "S":
      guess = (int)(input("Enter the index to reveal (between 0 and %d): " % (dim * dim - 1)))
      if not game.flip(guess):
        print("Selected location is already flipped!")
    else:
      print("Invalid option")
    game.check()

  game.render()
  print("Game lost!" if game.hasLost() else "Game won!")
  if input("Enter Q to quit: ") == "Q":
    break
