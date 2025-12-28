'''
We want to fill a disk with random 1's and 0's, but with a randomness
generated via a modified dragon curve. In particular, given an initial
sequence of 1's and 0's, we append its reversed and bit-flipped copy,
also putting a 0 between the two. We repeat this process until we have
enough data to fill the disk. We then compute the checksum of this random
sequence examining the equality of each non-overlapping pair of bits in it.
We recursively apply the calculation until the checksum is of odd length.
'''

from time import perf_counter


INIT_STATE_STR = "00101000101111010"


def expand(seed: bytearray, disk_len: int) -> bytearray:
    """
    Expand the dragon curve until disk_len is reached.
    Uses bytearray for compact storage and speed.
    """
    data = seed
    while len(data) < disk_len:
        n = len(data)
        data.append(0)
        # reversed and bit-flipped copy
        data.extend(1 - data[i] for i in range(n - 1, -1, -1))
    return data[:disk_len]


def checksum(data: bytearray) -> str:
    """
    Compute checksum iteratively until odd length.
    """
    while len(data) % 2 == 0:
        data = bytearray(
            1 if data[i] == data[i + 1] else 0
            for i in range(0, len(data), 2)
        )
    return ''.join('1' if b else '0' for b in data)


def solve(disk_len: int) -> str:
    seed = bytearray(int(c) for c in INIT_STATE_STR)
    data = expand(seed, disk_len)
    return checksum(data)


if __name__ == "__main__":
    start = perf_counter()
    print("Part 1 checksum:", solve(272))
    print("Elapsed:", perf_counter() - start)

    start = perf_counter()
    print("Part 2 checksum:", solve(35651584))
    print("Elapsed:", perf_counter() - start)

