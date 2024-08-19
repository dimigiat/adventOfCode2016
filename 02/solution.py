'''
* Retrieve a 5-digit code in the typical keypad
1 2 3
4 5 6
7 8 9
Each digit is provided in the instructions as a string of L/U/D/R 
characters to move around the keyboard. The starting point is "5" 
for the first digit and the last found digit for the rest of them.

** Same, but with the following keypad design
    1
  2 3 4
5 6 7 8 9
  A B C
    D
'''

with open('input.txt') as file:
    instructions = [item.strip() for item in file.readlines()]


# ----------------------- Part 1 ------------------------- #

digit = 5

solution_1 = []

for key in instructions:
    for move in key:
        if move == 'L':
            digit -= 0 if digit % 3 == 1 else 1
        elif move == 'R':
            digit += 0 if digit % 3 == 0 else 1
        elif move == 'U':
            digit -= 0 if (digit - 1) // 3 == 0 else 3
        elif move == 'D':
            digit += 0 if (digit - 1) // 3 == 2 else 3
    solution_1.append(digit)

print(solution_1)

# ----------------------- Part 2 ------------------------- #

solution_2 = []

# Grid radius of rhomb padlock
RADIUS = 2

MOVES = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, 1),
        "D": (0, -1)
    }


class RhombPoint:
    '''
    A point in a rhomb-shaped 2D grid with the maximum possible
    grid distance from (0, 0) being configurable as class attribute.
    '''

    radius = 1

    def set_radius(radius):
        RhombPoint.radius = int(radius)

    def is_valid(x, y):
        return abs(x) + abs(y) <= RhombPoint.radius

    def __init__(self, x, y):
        if not RhombPoint.is_valid(x, y):
            print("Provided coordinates fall outside", end=" ")
            print(f"current grid radius of {RhombPoint.radius}.")
            raise TypeError
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        return f"Rhombpoint({self.x},{self.y})"
    
    def __iadd__(self, move_string):
        '''Update point position given a L/R/U/D move'''
        move = MOVES[move_string]
        if RhombPoint.is_valid(self.x + move[0], self.y + move[1]):
            self.x += move[0]
            self.y += move[1]
        return self


def sign(num):
    '''Return the sign of a number as 0, 1 or -1'''
    return 0 if num == 0 else num // abs(num)

def get_digit(radius, x, y):
    '''
    Given a part 2 type rhomb padlock of arbitrary size, and
    the coordinates of a key, determine corresponding digit
    '''
    if abs(x) + abs(y) > radius:
        print(f"Invalid point coords for padlock of radius {radius}.")
        raise ValueError
    '''
    Consider the middle column. Moving from top row to center row
    increases the digit proportionally to the partial sums of the 
    positive integers series with factor 2, (i.e. 2,6,12,...), so we
    get n(n+1) change for n rows below top. By symmetry, moving from 
    bottom row to the center one has the same effect. Left/right 
    allowed moves between columns decrease/increase the digit by 1. 
    '''
    center_digit = 1 + radius * (radius + 1) # radius rows from top
    '''Absolute digit distance from being n rows away from center one
    is: radius * (radius + 1) - (radius - n) * (radius - n + 1). 
    Simplified, it becomes: n * (2 * radius - n + 1).''' 
    row_distance = abs(y) * ( 2 * radius - abs(y) +1 )
    digit = center_digit - sign(y) * row_distance + x
    return digit

# Setting rhomb grid dimension to the one of the padlock
RhombPoint.set_radius(RADIUS)

# Initial point corresponding to digit=5 for part 2
point = RhombPoint(-2, 0)

for key in instructions:
    for move in key:
        point += move
    digit = get_digit(RADIUS, point.x, point.y)
    solution_2.append((hex(digit)[2]).upper())

print(solution_2)