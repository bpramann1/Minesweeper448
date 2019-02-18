# Unimplemented Features

### Iterative approach to flipping tiles

We wanted to implement an iterative approach to flipping tiles because python
has a maximum recursion depth of 1000. This value is hit easily with the
current implementation and could be fixed with an iterative approach.
This feature would find all the tiles that need to be flipped and flip them
in one loop.

### Counter of flags placed versus how many can be placed

This feature would exist on the main game screen and would display
information about how many flags have been placed and how many flags need to
be placed in order to win.

### Scoring algorithm/leaderboard

This feature would be a way to compare a players performance throughout
different games. A scoring algorithm would have to decrease over time and would
depend on 'mine density' so larger boards 'dilute' the points you get by winning
more quickly. This would be displayed on a leaderboard that would persist
through restarts of the application. This was not an essential feature, so it
was not added in the time we had.