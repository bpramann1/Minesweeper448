#!/usr/bin/python3

#Testing flood fill algorithm to reveal tiles in response to user input
import random

dim = (int)(input("What dimensions do you want to use: "))
num_mines = (int)(input("How many mines do you want to plant: "))

mines = [0]*dim*dim
states = [0]*dim*dim
counts = [0]*dim*dim
count = 0

print(dim)
print(num_mines)

while count < num_mines:
  i = random.randint(0, dim*dim-1)
  print("Attempting to place mine in location: %d" % (i))
  if mines[i] != 1:
    print("Mine succesfully placed in location: %d" % (i))
    mines[i] = 1
    count += 1
  else:
    print("Attempt failed, selecting new location")

def begin_loop():
  endGame = False
  while (not endGame):
    display_board()
    guess = (int)(input("Select location to test (0 to %d): " % (dim*dim - 1)))
    if states[guess] == 0:
      if mines[guess] == 1:
        print("Mine triggered! End of game.")
        states[guess] = 1
        endGame = True
        break
      else:
        flip(guess)
    else:
      print("tile already revealed")
    
def display_board():
  accum = ""
  for i in range(0, dim*dim):
    if states[i] == 0:
      accum += "_, "
    elif states[i] == 1:
      if mines[i] == 1:
        accum += "M, "
      else:
        accum += (str)(counts[i]) + ", "
    if ((i % dim) == (dim - 1)):
      print(accum)
      accum = ""

def get_neighbors_indices(index):
  # top row
  if index < dim:
    # top left
    if index == 0:
      return([index + 1, index + dim, index + dim + 1])
    # top right
    if index == dim - 1:
      return([index - 1, index + dim - 1, index + dim])
    return([index - 1, index + 1, index + dim - 1, index + dim, index + dim + 1])
  
  # bottom row
  elif index // dim == (dim - 1):
    # bottom left
    if index % dim == 0:
      return([index - dim, index - dim + 1, index + 1])
    # bottom right
    if index % dim == (dim - 1):
      return([index - dim - 1, index - dim, index - 1])
    return[index - dim - 1, index - dim, index - dim + 1, index - 1, index + 1]
  
  # middle rows
  else:
    # left col
    if index % dim == 0:
      return([index - dim, index - dim + 1, index + 1, index + dim, index + dim + 1])
     # right col
    if index % dim == dim - 1:
      return([index - dim - 1, index - dim, index - 1, index + dim - 1, index + dim])
    return([index - dim - 1, index - dim, index - dim + 1, index - 1, index + 1, index + dim - 1, index + dim, index + dim + 1])

def count_mines(index):
  indices = get_neighbors_indices(index)
  s = 0
  for i in indices:
    s = s + mines[i]
  return s

for i in range(0, dim*dim):
  counts[i] = count_mines(i)

def flip(index):
  indices = get_neighbors_indices(index)
  states[index] = 1
  states[index] = 1
  if counts[index] == 0 and mines[index] == 0:
    for i in indices:
      if states[i] == 0:
        flip(i)

begin_loop()
