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

from time import perf_counter


def parsed_line(line: str) -> list[int]:
    return [int(i) for i in line.strip('.\n').split() if i.isdigit()]


def is_aligned(t: int, offset: int, initial: int, num_positions: int) -> bool:
    return (t + offset + initial) % num_positions == 0


def press_time(initials: tuple[int], num_positions: tuple[int]) -> int:
    '''
    Given the initial position of each disc, and the total number of its
    positions, return the number of seconds to wait before pressing the
    button to drop the capsule, so that the latter reaches all discs at
    their 0-th position.
    '''
    num_discs = len(initials)
    t = 0

    # Guaranteed to terminate because a solution exists for the given input
    while True:
        for disc in range(num_discs):
            if not is_aligned(t, disc + 1, initials[disc], num_positions[disc]):
                break
        else:
            return t
        t += 1


if __name__ == '__main__':

    with open('input.txt') as f:
        num_positions, initials = map(tuple, zip(*map(parsed_line, f)))

    # ---------------------------- Part 1 --------------------------------- #
    start = perf_counter()
    print(f'Part 1: Press at time: {press_time(initials, num_positions)}')
    stop = perf_counter()
    elapsed = stop - start
    print(f'Time elapsed: {elapsed} seconds.')

    # ---------------------------- Part 2 --------------------------------- #

    # One more disc added on top of the others for part 2.
    num_positions = (11,) + num_positions
    initials = (0,) + initials

    start = perf_counter()
    print(f'Part 2: Press at time: {press_time(initials, num_positions)}')
    stop = perf_counter()
    elapsed = stop - start
    print(f'Time elapsed: {elapsed} seconds.')



