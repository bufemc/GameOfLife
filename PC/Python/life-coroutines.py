
"""

Life with Coroutines - or Life with Corona times

Corona quarantine fun project: use coroutines, after reading chapter 40
of the book "Effective Python" (first edition) by Brett Slatkin,
and after working through a crash course in "Python's" data science stack.

Reducing the script to a minimum of lines is intended, to focus on coroutines.
The toroidal grid is filled initially with 3 gliders.

Credits: this script is derived on works of Mahesh Venkitachalam
https://github.com/electronut/pp/blob/master/conway/conway.py

"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import namedtuple


# Grid size (C64 column width 40) and update interval (fastest 1)
N = 40
INTERVAL = 1

# Cell values, using _ meaning a dead cell, not "any parameter"
LIFE = 255
DEAD = 0
CELL_VALUES = [LIFE, DEAD]

# Extra stuff to use coroutines consuming sent data
TICK = object()
Query = namedtuple('Query', 'y x')
Transition = namedtuple('Transition', 'y x state')

# Grid initialized here, so we don't have to pass it around
grid = np.zeros((N, N), dtype=int)


def addGlider(i, j, grid):
    """ Adds a glider https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life) """
    glider = np.array([[  0, 255,   0],
                       [  0,   0, 255],
                       [255, 255, 255]])
    grid[i:i+3, j:j+3] = glider


def count_neighbors(y, x):
    """ Return number of (toroidal) living cells for the 8 neighbor cells. """
    n_ = yield Query((y + 1) % N, (x + 0) % N)  # North
    ne = yield Query((y + 1) % N, (x + 1) % N)  # Northeast
    e_ = yield Query((y + 0) % N, (x + 1) % N)  # East
    se = yield Query((y - 1) % N, (x + 1) % N)  # Southeast
    s_ = yield Query((y - 1) % N, (x + 0) % N)  # South
    sw = yield Query((y - 1) % N, (x - 1) % N)  # Southwest
    w_ = yield Query((y + 0) % N, (x - 1) % N)  # West
    nw = yield Query((y + 1) % N, (x - 1) % N)  # Northwest
    neighbor_states = [s_, n_, w_, e_, nw, sw, se, ne]
    total = 0
    for state in neighbor_states:
        total += state
    return int(total / LIFE)


def game_logic(state, neighbors):
    """ Apply Conway's standard rules. """
    if state == LIFE and (neighbors < 2 or neighbors > 3):
        return DEAD
    elif neighbors == 3:
        return LIFE
    return state


def step_cell(y, x):
    """ First retrieves state of current cell, then of it's 8 neighbors.
    Gets next state of cell depending on neighbor count, then updates. """
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


def simulate():
    """ Loops through grid, TICK signals end of nested loop, will restart. """
    while True:
        for y in range(N):
            for x in range(N):
                yield from step_cell(y, x)
        yield TICK


def live_a_generation(new_grid, sim):
    """ Use the generator from simulate() to loop through the grid.
    For each cell send it's current state plus it's neighbors.
    If TICK signaled from simulate() one generation is over, update. """
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query): # Get information on this cell
            state = grid[item.y, item.x]
            item = sim.send(state)
        else:  # Must be a Transition
            new_grid[item.y, item.x] = item.state
            item = next(sim)
    return new_grid


def update_new(frame, img,):
    """ Update grid for one generation, prevent self-mutilation by copy. """
    new_grid = grid.copy()

    sim = simulate()
    new_grid = live_a_generation(new_grid, sim)

    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img


def main():
    addGlider(1, 1, grid)
    addGlider(5, 5, grid)
    addGlider(9, 9, grid)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update_new, fargs=(img,),
                                  frames=25,
                                  interval=INTERVAL)

    plt.show()


if __name__ == '__main__':
    main()
