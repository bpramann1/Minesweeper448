#!/usr/bin/python3

#Testing flood fill algorithm to reveal tiles in response to user input
import random

class Board:
  
  def __init__(self, dim, count):
    self.dim = dim
    self.lost = False
    self.active = True
    self.tiles = []
    self.mineIndices = []
    self.mineCount = count
    self.flagCount = 0

    # create a list of dim * dim unique tiles
    for n in range(0, dim * dim):
      self.tiles.append(Tile())
    
    # assign n tiles to be mines
    for n in range(0, count):
      while True:
        i = random.randint(0, dim*dim - 1)
        if not self.tiles[i].isMine():
          self.tiles[i].setMine()
          self.mineIndices.append(i)
          print("Setting mine at: %d" % (i)) 
          # increment the mine count on neighboring tiles
          for x in self.getNeighbors(i):
            self.tiles[x].incCount()
          break
  

  def getNeighbors(self, index):
    dim = self.dim
    above = index - dim
    below = index + dim
    indices = [above - 1, above, above + 1, index - 1, index + 1, below - 1, below, below + 1]
    if above < 0: # set above indices to None if on top row
      indices[0] = None
      indices[1] = None
      indices[2] = None
    if below >= dim * dim: # set below indices to None if on bottom row
      indices[5] = None
      indices[6] = None
      indices[7] = None
    if index % dim == 0: # set left indices to None if on left most col
      indices[0] = None
      indices[3] = None
      indices[5] = None
    if index % dim == dim - 1: # set right indices to None if on right most col
      indices[2] = None
      indices[4] = None
      indices[7] = None
    # filter out Nones from indices
    indices = filter(lambda x: not x is None, indices)
    # returns a filter type interable object usable in a for loop
    return indices
  
  # flip returns True if tile is revealed, even if it is a mine, but False if the tile has been revealed already
  def flip(self, index):
    if self.tiles[index].isFlipped():
      return(False)
    
    self.tiles[index].flip()
    
    if self.tiles[index].isMine():
      self.lost = True
      self.active = False
    elif self.tiles[index].getCount() == 0:
      for i in self.getNeighbors(index):
        self.flip(i)
    return(True)
  
  # toggle flagged state of tile at index
  def flag(self, index):
    if self.tiles[index].isFlipped():
      return(False)
    elif self.tiles[index].isFlagged():
      self.flagCount -= 1
      self.tiles[index].flag()
    elif self.mineCount == self.flagCount:
      return(False)
    else:
      self.flagCount += 1
      self.tiles[index].flag()
    return(True)


  def isActive(self):
    return self.active

  def hasLost(self):
    return self.lost
  
  def render(self):
    accum = ""
    dim = self.dim
    for (tile, index) in zip(self.tiles, range(0, dim * dim)):
      accum += tile.toString() + ", "
      if index % dim == -1 % dim:
        print(accum)
        accum = ""
  
  def check(self):
    for i in self.mineIndices:
      if not self.tiles[i].isFlagged():
        return(False)
    self.lost = False
    self.active = False
    return(True)

class Tile:
  def __init__(self):
    self.visible = False
    self.mine = False
    self.flagged = False
    self.count = 0
  
  def setMine(self):
    self.mine = True
  
  def incCount(self):
    self.count += 1
  
  def getCount(self):
    return(self.count)
  
  def isFlipped(self):
    return(self.visible)
  
  def isFlagged(self):
    return(self.flagged)

  def isMine(self):
    return self.mine
  
  def detectMine(self):
    if self.mine:
      self.visible = True
      return(True)
    return(False)
  
  def flag(self):
    self.flagged = not self.flagged
    return(self.flagged)

  def flip(self):
    self.visible = True
  
  def toString(self):
    if self.flagged:
      return("F")
    if self.visible and self.mine:
      return("M")
    if self.visible:
      return(" " if self.count == 0 else str(self.count))
    return("_")

if __name__ == "__main__":
  while True:
    dim = (int)(input("Enter dimensions for board: "))
    count = (int)(input("Enter number of mines: "))
    game = Board(dim, count)
    
    while game.isActive():
      game.render()
      type = (str)(input("Enter F to flag a mine, S an empty space: "))
      guess = (int)(input("Enter a guess index (between 0 and %d): " % (dim * dim - 1)))
      if type == "F":
        if not game.flag(guess):
          print("Selected location is already visible or too many flags are used")
      elif type == "S":
        if not game.flip(guess):
          print("Selected location is already flipped")
      game.check()
    
    game.render()
    print("Game lost!" if game.hasLost() else "Game won!")
    if input("Enter Q to quit: ") == "Q":
      break
