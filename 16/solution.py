'''
We want to fill a disk with random 1's and 0's, but with a randomness
generated via a modified dragon curve. In particular, given an initial
sequence of 1's and 0's, we append its reversed and bit-flipped copy,
also putting a 0 between the two. We repeat this process until we have
enough data to fill the disk. We then compute the checksum of this random
sequence examining the equality of each non-overlapping pair of bits in it.
We recursively apply the calculation until the checksum is of odd length.
'''

initState = list(map(bool, map(int, "00101000101111010")))

def processed(data, diskLen):
    while len(data) < diskLen:
        data = data + [False] + list(map(lambda x: not x, data[::-1]))
    return data[:diskLen]

def checksum(data):
    cksm = list(map(lambda x: x[0] == x[1], zip(data[::2], data[1::2])))
    if len(cksm) % 2 == 0:
        cksm = checksum(cksm)
    return cksm

print("Part 1 checksum:", end=" ")
print("".join(map(str, map(int, checksum(processed(initState, 272))))))

print("Part 2 checksum:", end=" ")
print("".join(map(str, map(int, checksum(processed(initState, 35651584))))))
