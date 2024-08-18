'''
In a 4x4 grid of rooms connected by doors, each door is open or closed
depending on the first four digits of the MD5 hash of a passcode augmented
with the path followed thus far (e.g. RDDL...) starting from top left.
The objective is to find the shortest path to the bottom right room.
'''

from hashlib import md5

'''
- Rooms are denoted by integers from 0-15, so that it's easy to get available
doors for each based on the quotient and remainder of division by 4.
Moving around rooms then translates to adding/subtracting 1 or 4.
- State of doors is represented by a boolean list of four elements for the
state in directions U, D, L, R.
'''

passcode = "pgflpeqp"
moveChars = ('U', 'D', 'L', 'R')
roomShifts = (-4, 4, -1, 1)

def isDoor(room):
    return [room // 4 != 0, room // 4 != 3, room % 4 != 0, room % 4 != 3]

def isOpen(path):
    currentHash = md5((passcode + path).encode()).hexdigest()
    # True if hex digit in b-f, False otherwise
    return [ord(i) in range(98, 103) for i in currentHash[:4]]

def getMoves(room, path):
    ''' Returns available moves as integer list (1->U, 2->D, 3->L, 4->R) '''
    doorState =  [a and b for a, b in zip(isDoor(room), isOpen(path))]
    return [ind for ind, val in enumerate(doorState) if val]

def shortestPath():
    rooms = [0] # current room for each path under examination
    paths = [""] # paths under examination
    while True:
        if not paths:
            return "Not found"
        room = rooms.pop(0)
        if room == 15:
            return paths[0]
        path = paths.pop(0)
        for move in getMoves(room, path):
            paths.append(path + moveChars[move])
            rooms.append(room + roomShifts[move])

def longestPath():
    found, longest = False, None
    rooms = [0] # current room for each path under examination
    paths = [""] # paths under examination
    while True:
        if not paths:
            if not found:
                return "Not found"
            return longest
        room = rooms.pop(0)
        if room == 15:
            longest = paths.pop(0)
            found = True
            continue
        path = paths.pop(0)
        for move in getMoves(room, path):
            paths.append(path + moveChars[move])
            rooms.append(room + roomShifts[move])


print(f"Part 1: Shortest path is {shortestPath()}")    
print(f"Part 2: Length of longest path is {len(longestPath())}")    

        