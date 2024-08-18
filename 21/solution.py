'''
Given an 8-character password, a sequence of given operations is 
performed to scramble their order. We are asked to find the scrambled 
version of a given password, and to unscramble another one.
NOTE: Although it's not stated as a requirement, the 'rotateBased'
operation needs passwords of unique characters to be unambiguously 
reversible regardless of the specific password.
'''

import re

ARGPATTERN = re.compile(r"\b[0-7a-h]\b")


def swapPosition(pswd, x, y, undo=False):
    chars = list(pswd)
    chars[x], chars[y] = chars[y], chars[x]
    return "".join(chars)

def swapLetter(pswd, x, y, undo=False):
    return pswd.replace(x, 'Z').replace(y, x).replace('Z', y)

def rotateLeft(pswd, steps, undo=False):
    steps = steps % 8
    if undo:
        return rotateRight(pswd, steps)
    else:
        return pswd[steps:] + pswd[:steps]

def rotateRight(pswd, steps, undo=False):
    steps = steps % 8
    if undo:
        return rotateLeft(pswd, steps)
    else:
        return pswd[-steps:] + pswd[:-steps]

def rotateBased(pswd, x, undo=False):
    ind = pswd.find(x)
    if undo:
        ind = getOldIndex(ind)
    shift = ind + 1 + ind // 4
    return rotateRight(pswd, shift, undo)

def reversePositions(pswd, x, y, undo=False):
    return pswd[:x] + pswd[x:y+1][::-1] + pswd[y+1:]

def movePosition(pswd, x, y, undo=False):
    if undo:
        x, y = y, x
    chars = list(pswd)
    chars.insert(y, chars.pop(x))
    return "".join(chars)

def getOldIndex(newIndex):
    '''
    Solution of the modular equation used in rotateBased for old index 
    old must be an integer in (0,7) for:
        old = 4/9 * (new - 1 + 8*c) + d/9,
        c in (0,2), 
        d in (0,3)
    '''
    for c in range(3):
        for d in range(4):
            q, r = divmod(4 * (newIndex - 1 + 8*c) + d, 9)
            if r == 0:
                return q 

def scrambled(password, instructions, undo=False):
    if undo:
        instructions = instructions[::-1]
    for instr in instructions:
        cmd = instr.split()[0] + instr.split()[1].capitalize()
        args = [int(c) if c.isdigit() else c 
                for c in re.findall(ARGPATTERN, instr)]
        password = eval(cmd)(password, *args, undo)
    return password


with open("input.txt") as f:
    instructions = f.readlines()

print(f"Part 1: {scrambled('abcdefgh', instructions)}")
print(f"Part 2: {scrambled('fbgdceah', instructions, undo = True)}")