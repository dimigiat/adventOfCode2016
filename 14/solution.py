'''
Given a salt string to be appended with an increasing integer index,
we are asked to find MD5 hashes which satisfy two conditions:
* Occurence of a three-of-a-kind sequence (e.g. ..aaa..), considering just
the first one, if multiple are present.
* Five-of-a-kind sequence with same character (e.g. ..aaaaa..) appearing
in at least one of the next 1000 hashes.
Specifically, the objective is to find the index which gives the 64th
hash that satisfies these conditions.
For part 1, we just apply MD5 once, for part 2 we apply it 2017 times.
'''

import re

from hashlib import md5
from functools import cache
from time import perf_counter
from typing import Callable


SALT_BYTES = 'ahsbgdzn'.encode()
TRIPLE_RE = re.compile(r'([0-9a-f])\1{2,}')
QUINTUPLE_RE = re.compile(r'([0-9a-f])\1{4,}')
LOOKAHEAD = 1000
TARGET_KEYS = 64
MD5_REPETITIONS = 2017


@cache
def md5_hash(index: int) -> str:
    '''
    Apply MD5 to a string created by appending the integer
    parameter to a constant string.
    '''
    return md5(SALT_BYTES + str(index).encode()).hexdigest()


@cache
def stretched_md5_hash(index: int) -> str:
    '''
    Apply MD5 hashing 2017 times in succession, starting from a string 
    created by appending the integer parameter to a constant string.
    '''
    res = md5_hash(index)
    for _ in range(MD5_REPETITIONS - 1):
        res = md5(res.encode()).hexdigest()
    return res


def target_index(hash_func: Callable[[int], str]) -> int:
    '''
    Given a function that takes an integer and returns a hex string, return the
    {TARGET_KEYS}'th integer that generates a string with 3 repeated characters 
    (e.g. 'aaa') and that character is repeated 5 times ('aaaaa') in the result
    of this function for at least one of the next LOOKAHEAD input integers.
    '''
    index, keys_count = -1, 0

    # For every hex character, we store the maximum index for which
    # we've found the character's quintuple in the function result
    last_quintuple_index = {c: 0 for c in '0123456789abcdef'}
    # Frontier tracks how far in indices we've searched for quintuples
    frontier = 0

    while keys_count < TARGET_KEYS:

        index += 1
        triple = TRIPLE_RE.search(hash_func(index))
        if not triple:
            continue
        triple_char = triple.group(1)

        # Look in the cache of quintuples first.
        # Cached indices are always <= (curr_index + 1 + LOOKAHEAD), 
        # we only need to check if they're larger than the current index.
        if last_quintuple_index[triple_char] > index:
            keys_count += 1
            continue

        # If not found a valid hit in the cache, scan up to LOOKAHEAD + 1
        # indices ahead. All indices <= frontier have been scanned for 
        # all quintuples, and hits cached, so they can be skipped.
        start = max(index + 1, frontier + 1)
        end = index + LOOKAHEAD + 1
        triple_matched = False

        for i in range(start, end):
            frontier = i
            for quintuple in QUINTUPLE_RE.finditer(hash_func(i)):
                q_char = quintuple.group(1)
                last_quintuple_index[q_char] = i
                if triple_char == q_char:
                    triple_matched = True
                    keys_count += 1
            # Don't exhaust the LOOKAHEAD window if we've matched the
            # triple with a quintuple. Doing so might examine unneeded hashes
            if triple_matched:
                break

    return index


if __name__ == '__main__':

    # ---------------------------- PART 1 ----------------------------------- #
    start = perf_counter()
    print(f'Part 1: Index for {TARGET_KEYS}th key: {target_index(md5_hash)}')
    stop = perf_counter()
    print(f'Finished in {stop - start} seconds')
    
    # ---------------------------- PART 2 ----------------------------------- #
    start = perf_counter()
    print(f'Part 2: Index for 64th key: {target_index(stretched_md5_hash)}')
    stop = perf_counter()
    print(f'Finished in {stop - start} seconds')

