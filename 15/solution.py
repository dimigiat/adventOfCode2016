'''
We have a set of rotating discs, each with a fixed number of positions
(different between discs). For each disc, one of its positions has a slot
through which a capsule may pass. We assume it's position 0 for all of them.
The discs are placed parallel to each other at equal vertical distances. 
We can drop a capsule with the push of a button, and it takes 1 sec for it 
to reach the 1st disc, another sec to reach the 2nd disc (assuming it passed 
the first through the slot), and so on. The discs rotate from each position
to the next with the same period of 1 sec.
Assuming we observe the position of discs at time=0, the objective is to find
the right time to press the button, for the capsule to go through all discs.

It can be formulated as the Chinese Remainder Theorem, if we don't 
want to try a brute force solution, like we do here.
(https://brilliant.org/wiki/chinese-remainder-theorem/)
'''

def parseLine(line):
    return [int(i) for i in line.strip(".\n").split() if i.isdigit()]

with open("input.txt") as f:
    numPositions, initials = map(list, zip(*map(parseLine, f)))

def discAtZero(offset, initial, numPositions, t):
    return (t + offset + initial) % numPositions == 0

def getPushTime(initials, numPositions):
    numDiscs = len(initials)
    offsets = list(range(1, numDiscs + 1))
    pushTime = 0
    while True:
        found = True
        for disc in range(numDiscs):
            if not discAtZero(offsets[disc], initials[disc],
                              numPositions[disc], pushTime):
                found = False
                break
        if found:
            return pushTime
        pushTime += 1

print(f"Part 1: Push button at time: {getPushTime(initials, numPositions)}")

numPositions.append(11)
initials.append(0)

print(f"Part 2: Push button at time: {getPushTime(initials, numPositions)}")



