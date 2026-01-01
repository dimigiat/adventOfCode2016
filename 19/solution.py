'''
Elves sitting in a circle bring one present each. Starting from elf 1, each elf
steals the present(s) of the next elf in the circle which is still in the game.
An elf whose presents are stolen gets eliminated. The last elf standing gets all
the presents. The goal is to find its index, given the initial number of elves.

For part 2, each elf steals presents from the elf right across the circle,
and in case there are two elves across, from the one on its left. Other
rules remain the same, we have to find the index of the winner again.
'''

'''
Part 1: A round starting with N elves ends with N//2 elves.
After round i, indices of remaining elves are spaced by 2^i.
After a round with even number of elves, the first elf still playing stays
the same. After a round with odd number of elves, the previously first elf
gets eliminated, so the first becomes firstIndex+2^i.
We observe that 2^i position increases match the binary representation
of a number, but we have to shift that number left as i starts from 1 and not
from 0. We find the winner via a masked left shift of N.

Note: This is a special case of a (N,k) Josephus problem, for k=2.
'''


def get_winner_1(n_elves: int) -> int:
    '''
    Take the binary representation of n_elves. Starting from the LSB, each
    1-valued bit represents an odd number as we repeatedly divide by 2. For
    each division, the first_elf's position increases by 2^(i+1), where i
    is the index of that bit. So, if we shift n_elves left once, each bit's
    value now represents the respective increase. We need to ignore the MSB,
    because we stop dividing once we end up with one elf, hence we mask the
    left shifted n_elves. The resulting integer now represents the aggregate
    position increase for the first elf, so adding 1 (the starting elf) to
    that, we get the position of the winning elf, which we return. 
    '''
    return 1 + (n_elves << 1) & ((1 << n_elves.bit_length()) - 1) 


'''
Part 2: A round that starts with N elves finishes with (N-1)//3 + 1.
So, for N initial elves, we have floor(log3(N-1)) rounds.
'''


def get_winner_2(n: int) -> int:
    '''
    The opposite elf moves as the circle shrinks.

    Let p be the largest power of 3 which is <= N
    The winner elf is:
    - If N == p  : N
    - If N <= 2p : N - p
    - Else       : 2N - 3p
    '''
    p = 1
    while p * 3 <= n:
        p *= 3

    if n == p:
        return n
    elif n <= 2 * p:
        return n - p
    else:
        return 2 * n - 3 * p


if __name__ == '__main__':

    print(f"Part 1: Winner elf is #{get_winner_1(3014603)}")
    print(f"Part 2: Winner elf is #{get_winner_2(3014603)}")