'''
Part 1:
Scan a list of strings to count those containing a four-character 
sequence made up of a pair of two different characters followed by
the reverse of that pair, but at the same time do not contain such a
sequence within a subsequence between square brackets. For example,
'abba[mnop]qrst' satisfies the criterion, while 'abcd[bddb]xyyx' does not.

Part 2:
Now count strings with an 'aba'-like three-character sequence outside square
brackets (two same characters with a different in-between), but also have
the same characters with reversed position ('bab') inside square brackets.
Note that the candidate 'aba' sequences might overlap in the same string. 
'''

# Note: All input strings contain at least one pair of square brackets

import re
from itertools import chain, tee
from typing import Iterator

def check_1(string: str) -> bool:
    '''
    Return True if string contains any 'abba'-like sequence outside
    square brackets, but none within. Else, return False.
    '''
    def is_abba(part: str) -> bool:
        '''True if argument string contains 'abba'-like sequence'''
        return bool(re.search(r'([a-z])(?!\1)([a-z])\2\1',part))
    parts = re.split(r'[\[\]]', string)
    return any(map(is_abba, parts[0::2])) and not any(map(is_abba, parts[1::2]))
        

def check_2(string: str) -> bool:
    '''
    If string contains any 'aba'-like sequence outside square brackets, and
    the mirror of it ('bab') within them, return True. Else, return False.
    '''
    def aba_iterator(part: str) -> Iterator[str]:
        ''' Iterator of possibly overlapping 'aba' sequences in a string'''
        return (match.group(1) for match in 
                # We use positive lookahead to consider possible overlaps
                re.finditer(r'(?=(([a-z])(?!\2)[a-z]\2))', part))
    def mirror(seq: str) -> str:
        return seq[1]+seq[0]+seq[1]
    parts = re.split(r'[\[\]]', string)
    # We chain all 'aba' occurences outside brackets in a single iterable
    # and we test if any of them appears mirrored within square brackets
    for aba in chain(*map(aba_iterator, parts[0::2])):
        if any(mirror(aba) in part for part in parts[1::2]):
            return True
    return False


def _self_test():
    assert check_1('abba[mnop]qrst')
    assert not check_1('abcd[bddb]xyyx')
    assert check_2('aba[bab]xyz')
    assert not check_2('xyx[xyx]xyx')


with open('input.txt') as file:

    _self_test()

    # Using itertools.tee for two independent file iterators
    iter_1, iter_2 = tee(file)
    print(sum(map(check_1, iter_1)))
    print(sum(map(check_2, iter_2)))