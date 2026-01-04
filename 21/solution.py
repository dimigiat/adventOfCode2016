'''
Given an 8-character password, a sequence of given operations is 
performed to scramble their order. We are asked to find the scrambled 
version of a given password, and to unscramble another one.
NOTE: Although it's not stated as a requirement, the 'rotate_based'
operation needs passwords of unique characters to be unambiguously 
reversible regardless of the specific password.
'''

import re

ARG_PATTERN = re.compile(r'\b(\d+|[a-z])\b')


def swap_position(pswd: str, x: int, y: int, *_) -> str:
    '''Swap the characters of pswd at indices x and y'''
    chars = list(pswd)
    chars[x], chars[y] = chars[y], chars[x]
    return ''.join(chars)


def swap_letter(pswd: str, x: str, y: str, *_) -> str:
    '''Swap characters x and y in pswd'''
    return pswd.replace(x, '*').replace(y, x).replace('*', y)


def rotate_left(pswd: str, steps: int, undo: bool=False) -> str:
    '''Rotate pswd cyclically steps positions to the left'''
    steps = steps % len(pswd)
    if undo:
        return rotate_right(pswd, steps)
    else:
        return pswd[steps:] + pswd[:steps]


def rotate_right(pswd: str, steps: int, undo: bool=False) -> str:
    '''Rotate pswd cyclically steps positions to the right'''
    steps = steps % len(pswd)
    if undo:
        return rotate_left(pswd, steps)
    else:
        return pswd[-steps:] + pswd[:-steps]


def rotate_based(pswd: str, x: str, undo: bool=False) -> str:
    '''
    Rotate pswd right one time, plus a number of times equal to the index of
    character x, plus one additional time if the index was at least 4.
    '''
    length = len(pswd)
    ind = pswd.index(x)
    if undo:
        ind = _invert_rotate_based(length, ind)
    shift = ind + 1 + (ind >= 4)
    return rotate_right(pswd, shift, undo)


def reverse_positions(pswd: str, x: int, y: int, *_) -> str:
    '''Reverse the part of pswd between positions x and y'''
    return pswd[:x] + pswd[x:y+1][::-1] + pswd[y+1:]


def move_position(pswd: str, x: int, y: int, undo: bool=False) -> str:
    '''Move character at position x in pswd to position y'''
    if undo:
        x, y = y, x
    chars = list(pswd)
    chars.insert(y, chars.pop(x))
    return ''.join(chars)


# Placed under function definitions as it refers to them
COMMANDS = {
    f.__name__: f
    for f in (
        swap_position,
        swap_letter,
        rotate_left,
        rotate_right,
        rotate_based,
        reverse_positions,
        move_position,
    )
}


def _invert_rotate_based(length: int, index: int) -> int:
    '''
    Given a password length and the new index after a rotate_based operation,
    return the original index of rotated character before rotation.
    '''
    for old in range(length):
        shift = 1 + old + (old >= 4)
        new = (old + shift) % length
        if new == index:
            return old
    raise ValueError(f'Invalid rotate_based index: {index}')


def scrambled(password: str, instructions: list[str], undo: bool=False) -> str:
    '''
    Given an initial password, apply all operations in a list of instructions
    in order, and return the resulting scrambled password. If undo=True,
    apply the inverse of each operation, iterating over them in reverse order
    and passing the undo=True flag to the respective functions, to finally
    return the unscrambled password.
    '''
    if len(password) != len(set(password)):
        raise ValueError('Password must contain unique characters')

    if undo:
        instructions = reversed(instructions)

    for instr in instructions:
        cmd = '_'.join(instr.split()[:2])
        args = [int(c) if c.isdigit() else c 
                for c in ARG_PATTERN.findall(instr)]
        if cmd in COMMANDS:
            password = COMMANDS[cmd](password, *args, undo)
        else:
            raise ValueError(f'Unknown instruction: {instr.strip()}')

    return password


if __name__ == '__main__':

    with open('input.txt') as f:
        instructions = f.readlines()

    print(f'Part 1: {scrambled('abcdefgh', instructions)}')
    print(f'Part 2: {scrambled('fbgdceah', instructions, undo = True)}')