'''
Given a salt string to be appended with an increasing integer index,
we are asked to find MD5 hashes which satisfy two conditions:
* Occurence of a three-of-a-kind sequence (e.g. ..aaa..).
* Five-of-a-kind sequence with same character (e.g. ..aaaaa..) appearing
in at least one of the next 1000 hashes.
Specifically, the objective is to find the index which gives the 64th
hash that satisfies these conditions.
For part 1, we just apply MD5 once, for part 2 we apply it 2017 times.
'''

import re

from hashlib import md5
from functools import cache


salt = 'ahsbgdzn'


@cache
def getHash(index):
    return md5((salt + str(index)).encode()).hexdigest()

@cache
def getStretchedHash(index):
    res = salt + str(index)
    for _ in range(2017):
        res = md5(res.encode()).hexdigest()
    return res

def get64thKey(hashFunc):
    index, keysCount = 0, 0
    while keysCount < 64:
        triple = re.search(r'([0-9a-f])\1\1', hashFunc(index))
        if triple:
            for i in range(index+1, index+1001):
                if re.search(triple.group(1) * 5, hashFunc(i)):
                    keysCount += 1
                    break
        index += 1
    return index - 1


print(f"Part 1: Index giving 64th key: {get64thKey(getHash)}")
print(f"Part 2: Index giving 64th key: {get64thKey(getStretchedHash)}")


