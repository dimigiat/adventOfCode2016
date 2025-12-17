'''
Part 1:
We have a screen of 6x50 pixels, all of which are initially OFF.
We can apply three types of operations to it:
- rect AxB: Turn on all pixels of top left BxA rectangle.
- rotate row y=A by B: shift all pixels in row A (starting by 0) right
by B pixels, pixel on the right end appearing on the left end.
- rotate column x=A by B: shift all pixels in column A (starting by 0) down
by B pixels, pixel on the bottom appearing on the top.
We must find how many pixels are lit after a given sequence of intsructions.

Part 2:
Figure out the sequence of capital letters the screen depicts after the
instructions, where each letter is 5 pixels wide and 6 tall.
'''

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import re

def rect(screen: npt.NDArray[np.bool_], y: int, x: int) -> None:
    '''Given a boolean 2D array, set its top left x-by-y items to True'''
    if screen.ndim != 2:
        raise ValueError("screen must be 2-dimensional")
    # Arguments are "wide" and "tall", so reversed to
    # correspond to rows and columns in array
    screen[0:x,0:y] = True


def rotate_row(screen: np.ndarray, row: int, shift: int) -> None:
    '''Shift items in a row of a 2D array right by a number of positions'''
    if screen.ndim != 2:
        raise ValueError("screen must be 2-dimensional")
    screen[row, :] = np.roll(screen[row, :], shift)


def rotate_column(screen: np.ndarray, column: int, shift: int) -> None:
    '''Shift items in a column of a 2D array down by a number of positions'''
    if screen.ndim != 2:
        raise ValueError("screen must be 2-dimensional")
    screen[:,column] = np.roll(screen[:,column], shift)


# Map instruction strings to functions; must come after function definitions
ACTIONS = {
    'rect': rect,
    'rotate row': rotate_row,
    'rotate column': rotate_column
}

def follow_instruction(screen: np.ndarray, instruction: str) -> None:
    '''Read a single instruction string and configure pixels appropriately'''
    action = re.match(r'(rect|rotate row|rotate column)', instruction).group()
    args = map(int, re.findall(r'\d+', instruction))
    ACTIONS[action](screen, *args)


if __name__ == '__main__':

    screen = np.zeros([6,50], dtype=bool)

    with open('input.txt') as f:
        for instruction in f: 
            follow_instruction(screen, instruction)

    # ------- Part 1 ------ #
    print(f"Part 1: Number of lit pixels: {screen.sum()}.")
    print('-'*40)

    # ------- Part 2 ------ #
    print('Part 2: Screen view after instructions:')
    print()

    # View screen without matplotlib
    for row in screen:
        print(''.join('#' if pixel else ' ' for pixel in row))

    # View screen using matplotlib
    plt.imshow(screen, cmap="copper_r")
    plt.axis("off")
    plt.show()