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

def check_1(string):
    '''
    Return True if string contains any 'abba'-like sequence outside
    square brackets, but none within. Else, return False.
    '''
    def abba(part):
        '''True if argument string contains 'abba'-like sequence'''
        return bool(re.search(r'([a-z])(?!\1)([a-z])\2\1',part))
    parts = re.split(r'[\[\]]', string)
    return any(map(abba, parts[0::2])) and not any(map(abba, parts[1::2]))
        

def check_2(string):
    '''
    If string contains any 'aba'-like sequence outside square brackets, and
    the mirror of it ('bab') within them, return True. Else, return False.
    '''
    def aba(part):
        ''' Iterator of possibly overlapping 'aba' sequences in a string'''
        return (match.group(1) for match in 
                # We use positive lookahead to consider possible overlaps
                re.finditer(r'(?=(([a-z])(?!\2)[a-z]\2))', part))
    def mirror(seq):
        return seq[1]+seq[0]+seq[1]
    parts = re.split(r'[\[\]]', string)
    # We chain all 'aba' occurences outside brackets in a single iterable
    # and we test if any of them appears mirrored within square brackets
    for seq in chain(*map(aba, parts[0::2])):
        if any(map(lambda part: mirror(seq) in part, parts[1::2])):
            return True
    return False


with open('input.txt') as file:
    # Using itertools.tee for two independent file iterators
    iter_1, iter_2 = tee(file)
    print(sum(map(check_1, iter_1)))
    print(sum(map(check_2, iter_2)))