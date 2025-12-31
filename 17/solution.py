'''
In a rectangular grid of rooms connected by doors, a door in direction U/D/L/R
is open/closed depending on the first 4 digits of the MD5 hash of a passcode
augmented with the path thus far (e.g. RDDL...). The objective is to find:
i) the shortest path from a starting room to a goal room.
ii) the length of the longest path from a starting room to a goal room, with
the note that once a path reaches the goal room it ends there.
'''

from hashlib import md5
from collections import deque
from functools import cache


PASSCODE_BYTES = 'pgflpeqp'.encode()
MOVE_CHARS = 'UDLR'
N_ROWS = 4
N_COLS = 4

# Rooms assigned increasing integers (0, 1, ...) as we scan the grid row-wise 
ROOM_SHIFTS = dict(zip(MOVE_CHARS, (-N_COLS, N_COLS, -1, 1)))
START_ROOM = 0
GOAL_ROOM = N_ROWS * N_COLS - 1


@cache
def is_door(room: int) -> tuple[bool, bool, bool, bool]:
    '''
    Return tuple of booleans telling us if room has door in direction (U,D,L,R).
    '''
    return (
        room // N_COLS != 0, 
        room // N_COLS != N_ROWS - 1, 
        room % N_COLS != 0, 
        (room + 1) % N_COLS != 0
    )


def is_open(path: str) -> tuple[bool, bool, bool, bool]:
    '''
    We append the path until the current room to PASSCODE, and take the 
    first 4 characters of the resulting MD5 hash, corresponding to 
    potentially existing doors in UDLR order. Such a door is open if the hex character is in [bcdef], closed otherwise. Return as tuple of booleans.
    '''
    curr_hash = md5(PASSCODE_BYTES + path.encode()).hexdigest()
    return tuple(i in 'bcdef' for i in curr_hash[:4])


def door_states(room: int, path: str) -> tuple[bool, bool, bool, bool]:
    '''
    For a room specified by both its integer room ID and the path
    that led to it, return which doors are usable in UDLR order.
    '''
    grid_doors = is_door(room)
    hash_doors = is_open(path)
    return tuple(a and b for a, b in zip(grid_doors, hash_doors))


def moves(room: int, path: str) -> tuple[str, ...]:
    ''' 
    For a given room and the path followed to get to the room, return
    available moves as a tuple of characters for those directions (U/D/L/R).
    '''
    states = door_states(room, path)
    return tuple(MOVE_CHARS[i] for i, open_ in enumerate(states) if open_)


def shortest_path() -> str|None:
    '''
    Return shortest path from top left to bottom right room in the grid.
    Unlike typical shortest path problems, we cannot filter rooms if they
    have been already visited, as each distinct path generally corresponds
    to a different state of the doors in the grid.
    '''

    # Queue of rooms as (room_id, path)
    queue = deque([(START_ROOM, '')])
    
    while queue:
        room, path = queue.popleft()
        if room == GOAL_ROOM:
            return path
        for move in moves(room, path):
            queue.append((room + ROOM_SHIFTS[move], path + move))


def longest_path_length() -> int:
    '''
    Return length of longest path from top left to bottom right room in the
    grid. The idea is that we keep searching until there is no path that can 
    be extended, and update the target length whenever we reach the goal room.
    '''

    longest = -1

    # Queue of rooms as (room_id, path)
    stack = deque([(START_ROOM, '')])

    while stack:
        room, path = stack.pop()
        if room == GOAL_ROOM:
            longest = max(longest, len(path))
            # Don't extend paths that reached goal room
            continue
        for move in moves(room, path):
            stack.append((room + ROOM_SHIFTS[move], path + move))

    return longest


if __name__ == '__main__':

    print('Part 1:', end= ' ')
    path = shortest_path()
    if path is not None:
        print(f'Shortest path is {path}')
    else:
        print('No valid way to reach goal room.')

    print('Part 2:', end = ' ')
    longest = longest_path_length()
    if longest >= 0: 
        print(f'Length of longest path is {longest}')
    else:
        print('No valid way to reach goal room.')