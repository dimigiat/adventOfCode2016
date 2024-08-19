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
import re

screen = np.zeros([6,50], dtype=bool)

def rect(y, x):
    # Arguments are "wide" and "tall", so reversed to
    # correspond to rows and columns in array
    screen[0:x,0:y] = True

def rotate_row(row, shift):
    screen[row, :] = np.roll(screen[row, :], shift)

def rotate_column(column, shift):
    screen[:,column] = np.roll(screen[:,column], shift)

def follow_instruction(instruction):
    '''Read a single instruction string and configure pixels appropriately'''
    action = re.match(r'(rect|rotate row|rotate column)', instruction).group()
    args = map(int, re.findall(r'\d+', instruction))
    eval(action.replace(' ','_'))(*args)

with open('input.txt') as f:
    for instruction in f: 
        follow_instruction(instruction)
        
print(f"Part 1: Number of lit pixels: {screen.sum()}.")
print('-'*40)

# ------- Part 2 ------ #

print('Part 2: Screen view after instructions:')
print()

# View screen without matplotlib
translate = {True:'.', False:' '}
for row in screen:
    for elem in row:
        print(translate[elem], end='')
    print()

# View screen using matplotlib
from matplotlib import pyplot as plt
im = plt.imshow(screen, cmap="copper_r")

