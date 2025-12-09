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

from collections import deque, defaultdict
import re


def process_instruction(
        instruction: str, 
        bots: defaultdict[int, list[int]], 
        outputs: dict[int, int]
) -> bool:
    '''Execute instruction and return True if the source
    is either an input chip or a bot for which both its
    values are already known. Else, return False'''

    if instruction.startswith('value'):
        val, bid = map(int, re.findall(r'\d+', instruction))
        bots[bid].append(val)
        return True
    else:
        bid = int(re.search(r'\d+', instruction).group())
        if len(bots[bid]) == 2:
            # Bot has both values, we can carry out instruction
            low, high = sorted(bots[bid])
            low_t, high_t = re.findall(r'(output|bot)', instruction)[1:]
            low_id, high_id = map(int, re.findall(r'\d+', instruction)[1:])
            if low_t == 'bot':
                bots[low_id].append(low)
            else:
                outputs[low_id] = low
            if high_t == 'bot':
                bots[high_id].append(high)
            else:
                outputs[high_id] = high
            return True
        else:
            # Revisit this instruction when bot has both values
            return False

if __name__ == '__main__':

    outputs = {}  # int: int
    bots = defaultdict(list)  # int: list[int]

    with open('input.txt') as f:
        instruction_queue = deque(f.readlines())
        while instruction_queue:
            instruction = instruction_queue.popleft()
            if not process_instruction(instruction, bots, outputs):
                instruction_queue.append(instruction)
            
    # Part 1
    for bid, values in bots.items():
        if sorted(values) == [17, 61]:
            print(bid)

    # Part 2
    print(outputs[0] * outputs[1] * outputs[2])