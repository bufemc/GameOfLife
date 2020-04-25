
"""

Life simple - or Life within Corona times

A small quarantine fun project: try to write Conway's Game of Life,
still with a toroidal grid, and filled randomly on start after working
through a crash course about the data science stack available for Python.

WARNING! Normally it's a very bad idea to use _ as a variable name, it's
normally used in Python as a placeholder, but ok to assign on the right side.

Credits: this script is derived on works of Mahesh Venkitachalam
https://github.com/electronut/pp/blob/master/conway/conway.py

"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Grid size (C64 column width 40) and update interval (fastest 1)
N = 40
INTERVAL = 1

# Cell values, using _ meaning a dead cell, not "any parameter"
o = 255
_ = 0
CELL_VALUES = [o, _]


def update(frame, img, grid, N):
    """ Update grid for one generation, prevent self-mutilation by copy. """
    new_grid = grid.copy()

    for i in range(N):
        for j in range(N):
            total = (grid[i, (j - 1) % N] + grid[i, (j + 1) % N]
                     + grid[(i - 1) % N, j] + grid[(i + 1) % N, j]
                     + grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N]
                     + grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / o

            if grid[i, j] == o and (total < 2 or total > 3):
                new_grid[i, j] = _
            elif total == 3:
                new_grid[i, j] = o

    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img


def main():
    grid = np.random.choice(CELL_VALUES, N * N, p=[0.25, 0.75]).reshape(N, N)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N),
                                  frames=25,
                                  interval=INTERVAL)

    plt.show()


if __name__ == '__main__':
    main()
