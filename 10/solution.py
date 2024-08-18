'''
A set of microchips, each with a unique integer value, are connected 
to a set of output slots, also with (independent) integer IDs. The 
connection takes place via a mesh of bots, each with 2 inputs and 2 
outputs. A bot input can be attached to directly a chip or to another    
bot's output. Each bot's routing decision depends on the chip values, 
one output is for the higher one, the other for the lower one. Routing 
and link topology are described in a sequence of instructions.
--------------------
Part 1:
Find which chip will route value-61 and value-17 microchips.
--------------------
Part 2:
Multiply values of microchips in outputs 0, 1 and 2.
'''

import re


def process_instruction(line):
    # Newly encountered bots are added with empty list values       
    for bot in re.finditer(r'bot (\d+)', line):
        id = int(bot.group(1))
        if id not in bots:
            bots[id] = []

    line = line.split(' ')
    if line[0] == 'value':
        val, id = int(line[1]), int(line[5])
        bots[id].append(val)
        return True
    else:
        id = int(line[1])
        if len(bots[id]) == 2:
            # Bot has both values, we can carry out instruction
            low, high = sorted(bots[id])
            low_id, high_id = int(line[6]), int(line[11])
            if line[5] == 'bot':
                bots[low_id].append(low)
            else:
                outputs[low_id] = low
            if line[10] == 'bot':
                bots[high_id].append(high)
            else:
                outputs[high_id] = high
            return True
        else:
            # We'll revisit this line when bot has both values
            return False


outputs = {}  # int: int
bots = {}  # int: list

with open('input.txt') as f:
    instructions = f.readlines()
    while instructions:
        instructions = [i for i in instructions if not process_instruction(i)]

# Part 1
for id in bots:
    if sorted(bots[id]) == [17, 61]:
        print(id)

# Part 2
print(outputs[0] * outputs[1] * outputs[2])