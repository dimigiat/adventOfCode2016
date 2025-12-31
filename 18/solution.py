'''
In a tile floor arranged in rows of fixed length, some tiles are traps ('^')
and the rest are safe ('.'). Given the tile status of the first row, whether
a tile in any row below that is safe is determined by given rules about the
values of two of the three tiles just above it (left up, right up).
We're asked to count the safe tiles for 40 and for 400000 rows. 
'''

from time import perf_counter


def safe_cnt_bitwise(n_rows: int, first: str) -> int:
    '''
    Count safe tiles using bitwise row representation.
    
    A tile is a trap if left and right tiles above differ; otherwise safe.
    '''
    width = len(first)
    
    # Convert first row to integer: 1 = trap (^), 0 = safe (.)
    row = 0
    for c in first:
        row = (row << 1) | (1 if c == '^' else 0)
    
    mask = (1 << width) - 1  # keeps row within width
    safe_count = width - bin(row).count('1')  # safe tiles in first row

    for _ in range(1, n_rows):
        # next row = 1 where left != right
        next_row = ((row >> 1) ^ (row << 1)) & mask
        safe_count += width - bin(next_row).count('1')
        row = next_row

    return safe_count


if __name__ == '__main__':

    with open('input.txt') as f:
        first = f.read().strip()

    start = perf_counter()
    print(f'Part 1: {safe_cnt_bitwise(40, first)} safe tiles in 40 first rows.')
    print(f'Elapsed: {perf_counter() - start:.4f} seconds.')

    start = perf_counter()
    print(f'Part 2: {safe_cnt_bitwise(400000, first)} safe tiles in 400000 first rows.')
    print(f'Elapsed: {perf_counter() - start:.4f} seconds.')
