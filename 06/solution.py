'''
Part 1:
Given a sequence of N-character strings, we must find the most frequent
character per string position, and combine them into a new string.

Part 2:
Same, but now considering the least frequent character per position.
'''

from collections import Counter as Cnt

with open('input.txt') as file:
    counts = map(Cnt.most_common, map(Cnt, zip(*file)))
    for sol in zip(*((c[0][0],c[-1][0]) for c in counts)):
        print(''.join(sol).strip())