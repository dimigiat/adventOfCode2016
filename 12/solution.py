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


# Change value of 'c' to 1 for part 2
register = dict(zip(('a', 'b', 'c', 'd'), (0, 0, 0, 0)))
current = 0

def cpy(x, y):
    register[y] = register[x] if x in register else eval(x)
    return 1

def inc(x):
    register[x] += 1
    return 1

def dec(x):
    register[x] -= 1
    return 1

def jnz(x, y):
    if x in register:
        return eval(y) if register[x] != 0 else 1
    else:
        return eval(y) if eval(x) else 1
        

with open('input.txt') as f:
    instructions = f.readlines()
    while current < len(instructions):
        instr = instructions[current].split()
        cmd, args = instr[0], instr[1:]
        current += eval(cmd)(*args)   

print(register)