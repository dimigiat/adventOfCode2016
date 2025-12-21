'''
Part 1:
The compressed form of a string uses interpolated markers of form '(MxN)',
meaning that the next M characters are repeated N times in the original text.
If a marker sequence falls into the data referenced by a previous marker, it
is treated as simple data, e.g. (5x2)(2x2)A --> (2x2)(2x2)A 
We're asked to find the length of the decompressed string.

Part 2:
Now markers that lie in the data referenced by a previous marker must be also
decompressed. Once again, we must find the length of the decompressed string.
'''

import re

PATTERN = re.compile(r'\((\d+)x(\d+)\)')


def len_decompressed_1(text: str) -> int:
    '''
    Scan a string for markers of type (MxN), with M, N positive integers.
    Starting with an integer equal to the length of the string, whenever 
    a match is found, add to that M*(N-1) minus the number of characters in 
    the marker, and resume scanning from M positions after the marker.
    Return the final value of that integer, which represents the length of the
    decompressed string, according to the rules for part 1. 
    '''
    count = len(text)
    pos = 0

    while mark := PATTERN.search(text, pos):
        m, n = int(mark.group(1)), int(mark.group(2))
        start, end = mark.start(), mark.end()
        count += m * (n - 1) - (end - start)
        pos = end + m 

    return count


def len_decompressed_2(text: str) -> int:
    '''
    Return length of the decompressed string for part 2. Makes use of a
    recursive private function that acts on any substring. 
    '''
    return _len_range(text, 0, len(text))


def _len_range(text: str, start: int, end: int) -> int:
    '''
    Given a string, a start index and an end index, the decompressing rules
    of part 2 are applied to the respective substring. The function is called 
    recursively as necessary to take all nested markers into account.
    It returns the decompressed length of the substring.
    '''
    count = 0
    pos = start

    while pos < end:
        if not (mark := PATTERN.search(text, pos, end)):
            # No more markers in this range
            count += end - pos
            break

        # Characters before marker
        count += mark.start() - pos

        m, n = int(mark.group(1)), int(mark.group(2))

        data_start = mark.end()
        data_end = data_start + m

        # Recursively compute the length of the referenced data
        chunk_len = _len_range(text, data_start, data_end)

        count += chunk_len * n

        pos = data_end

    return count


if __name__ == '__main__':

    with open('input.txt') as f:
        text = f.read().strip()

    print(len_decompressed_1(text))
    print(len_decompressed_2(text))