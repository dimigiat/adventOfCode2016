'''
We are located at point A in a street grid and are given instructions that
ultimately lead us to point B. Each instruction tells us to turn left or right,
then walk straight for a number of blocks (e.g. L3, R4, R2).
Input is a string with instructions separated with ", ".
Objectives:
* Compute the grid shortest distance from A to B
** Find the grid distance of A and the first location where the 
itinerary line crosses itself (i.e. first location visited twice)
'''

# We could simply use tuples for the coordinates. 
# We chose to implement some classes for practice purposes.

class Vector:
    def __init__(self, x, y):
        self.x = x 
        self.y = y

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, vector):
        '''Add a vector to the point'''
        if not isinstance(vector, Vector):
            raise TypeError("Point.__add__ only accepts Vector")
        return Point(self.x + vector.x, self.y + vector.y)

    # Not the wisest design choice to implement __iadd__, as a Point is
    # conceptually immutable. It can also lead to bugs (see comment in
    # function part_2 below). Again, it's mostly for practicing how this
    # magic method can be implemented for a custom class.
    def __iadd__(self, vector):
        '''Add a vector to the point in-place'''
        if not isinstance(vector, Vector):
            raise TypeError('Point.__iadd__ only accepts Vector')
        self.x += vector.x
        self.y += vector.y
        # x += y is equivalent to x = x.__iadd__(y), so we return self
        return self 
        
    def __eq__(self, other):
        '''Check for equality with other point'''
        if not isinstance(other, Point):
            print('Can not compare Point object with non-Point object')
            raise TypeError
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'


def part_1(instructions: list[str]) -> int:
    '''
    Given a list of strings for rotation and distance of each move, we
    start from point (0,0) and return the end point's coordinates.
    '''
    coords = Point(0, 0)
    direction = 0 # 0->North, 1->East, 2->South, 3->West
    for instr in instructions:
        direction = (direction + (1 if instr[0] == "R" else -1)) % 4
        distance = int(instr[1:])
        v_x = (direction % 2) * (-1) ** (direction // 2) * distance
        v_y = ((direction + 1) % 2) * (-1) ** (direction // 2) * distance 
        vector = Vector(v_x, v_y)
        coords += vector
    return abs(coords.x) + abs(coords.y)


def part_2(instructions: list[str]) -> int | None:
    '''
    Given a list of strings for rotation and distance of each move, we start
    from point (0,0) and return the coordinates of the first point visited
    twice, or None if the itinerary never crosses itself.
    '''
    current_point = Point(0, 0)
    visited = {Point(0, 0)}
    direction = 0 # 0->North, 1->East, 2->South, 3->West
    for instr in instructions:
        direction = (direction + (1 if instr[0] == "R" else -1)) % 4
        distance = int(instr[1:])
        # Move one block at a time, check if revisited
        for _ in range(1, distance + 1):
            # unit vector will be one of (1,0), (-1,0), (0,1), (0,-1) 
            v_x = (direction % 2) * (-1) ** (direction // 2)
            v_y = ((direction + 1) % 2) * (-1) ** (direction // 2)  
            vector = Vector(v_x, v_y)
            # We don't use the += notation because it modifies the last 
            # added item of the visited set in place, making it equal
            # to the new object. So, the check below would return true 
            # immediately from the first block.
            current_point = current_point + vector
            if current_point in visited:
                return abs(current_point.x) + abs(current_point.y)
            visited.add(current_point)
    return None


if __name__ == '__main__':
    with open('input.txt') as f:
        instructions = f.read().strip().split(', ')

    res_1, res_2 = part_1(instructions), part_2(instructions)
    print(res_1, res_2 if res_2 else 'No position revisited')