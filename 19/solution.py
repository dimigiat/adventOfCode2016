'''
Elves are sitting in a circle and bring one present each. Starting from
elf 1, each elf steals the present(s) of the next elf in the circle which
is still in the game. An elf whose presents are stolen, automatically gets
eliminated. In the end, one elf gets all the presents. The goal is to find
its index, given the initial number of elves.

For part 2, each elf steals a present from the elf right across the circle,
and in case there are two elves across, from the one on its left. Other
rules remain the same, we have to find the index of the winner again.
'''

from math import log2

'''
Part 1: A round starting with N elves ends with N//2 elves.
Thus, for a given initial N, we have floor(log2(N)) rounds.
After round i, indices of remaining elves are spaced by 2^i.
After a round with even number of elves, the first elf still playing stays
the same. After a round with odd number of elves, the previously first elf
gets eliminated, so the first becomes firstIndex+2^i.
It follows we just have to monitor the number of elves at each round and
keep track of the first index, whose final value will be the winner.

This case admits a closed form solution (cf. Josephus Problem), and even a
neat implementation via a 1-bit cyclic shift of the binary representation of N.
'''

def getWinner1(numElves):
    firstElf = 1
    for round in range(1, int(log2(numElves))+1):
        if numElves % 2 == 1:
            firstElf = firstElf + 2**round
        numElves = numElves // 2


'''
For part 2, a round that starts with N elves finishes with (N-1)//3 + 1.
So, for N initial elves, we have floor(log3(N-1)) rounds.
The solution below has been borrowed from a reddit user.
'''

def getWinner2(numElves):
    largest = 1
    working = 1
    for current in range(1, numElves + 1):
        if working + 2 > current:
            largest = working
            working = 1
        elif working < largest:
            working += 1
        else:
            working += 2
    return working

print(f"Part 1: Winner elf is #{getWinner1(3014603)}")
print(f"Part 2: Winner elf is #{getWinner2(3014603)}")
#---------------------------------------------------------

'''
2 -> 1

3 -> 3

4 -> 1, 2
     1

5 -> 2, 4
     2

6 -> 3, 6
     3

7 -> 1, 3, 5
     5

8 -> 2, 4, 7
     7

9 -> 3, 6, 9
     9

10 -> 1, 4, 5, 8
      1, 4
      1

11 -> 2, 5, 7, 10
      2, 5
      2

12 -> 3, 6, 9, 12
      3, 6
      3

13 -> 1, 4, 6, 8, 11
      4, 8
      4

14 -> 2, 5, 7, 10, 13
      5, 10
      5

15 -> 3, 6, 9, 12, 15
      6, 12
      6

16 -> 1, 4, 7, 8, 11, 14
      7, 14
      7

17 -> 2, 5, 8, 10, 13, 16
      8, 16
      8

18 -> 3, 6, 9, 12, 15, 18
      9, 18
      9

19 -> 1, 4, 7, 9, 11, 14, 17
      1, 7, 11
      11
'''