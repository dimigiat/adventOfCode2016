'''
We're given a sequence of instructions written in an assembly-type
code, operating on four registers (a, b, c, and d) that start at 0
and can hold any integer. The language uses the following instructions:
- cpy x y: copy x (an integer or the value of a register) into register y.
- inc x: increase the value of register x by one.
- dec x: decrease the value of register x by one.
- jnz x y: jump to an instruction y away, but only if x is not zero.

Part 1: Determine value of register a, after executing input instructions.

Part 2: Same, but with register c initialized with 1.
'''

from typing import Literal


def value(register: dict[str, int], x: str) -> int:
    return register[x] if x in register else int(x)


def cpy(register: dict[str, int], x: str, y: str) -> Literal[1]:
    register[y] = value(register, x)
    return 1


def inc(register: dict[str, int], x: str) -> Literal[1]:
    register[x] += 1
    return 1


def dec(register: dict[str, int], x: str) -> Literal[1]:
    register[x] -= 1
    return 1


def jnz(register: dict[str, int], x: str, y: str) -> int:
    return value(register, y) if value(register, x) else 1
        

# Defined after function definitions because it refers to them
COMMAND = {
    "cpy": cpy,
    "inc": inc,
    "dec": dec,
    "jnz": jnz
}


def run(instructions: list[list[str]], register: dict[str, int]) -> None: 
    '''
    Given a list of instructions and the initial values of a set of registers,
    execute instructions, modifying the register values in-place. Stop when
    index for next instruction gets beyond the number of instructions.
    '''
    current = 0
    while current < len(instructions):
        cmd, *args = instructions[current]
        current += COMMAND[cmd](register, *args)


if __name__ == '__main__':

    with open('input.txt') as f:
        instructions = [line.strip().split() for line in f]

    # --------------- Part 1 -----------------
    register = dict.fromkeys("abcd", 0)
    run(instructions, register)
    print(register)

    # --------------- Part 2 -----------------
    register = dict.fromkeys("abcd", 0)
    register['c'] = 1
    run(instructions, register)
    print(register)