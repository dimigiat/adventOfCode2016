'''
Part 1:
We are given an input string and are asked to calculate an eight 
character password as follows. Each character is the MD5 hash of 
the input and an increasing integer (as a string, starting at 0). 
If the hex representation of the hash starts with five zeros, 
the sixth hash character is the next character of the password. 
So we must find the eight first hashes which satisfy this criterion. 

Part 2:
Same, but now we're looking for hashes starting with five zeros and whose
sixth character is 0-7 indicating the position in the password, the 
character itself being the seventh in a matching hash. For each position, 
only the first occurrence of a matching hash is taken into account.
'''

# Reminder: MD5 function accepts byte sequence, returns 128 bit hash value.

from hashlib import md5
from itertools import count
from time import time


def get_hash(prefix: bytes, number: int) -> str:
    '''Append an integer to a bytes object, and return its MD5 hash in hex'''
    return md5(prefix + str(number).encode()).hexdigest()


if __name__ == '__main__':
 
    # Since input only features ASCII characters, we can use a bytes literal. 
    input_string = b'ffykfhsq'

    # ------------ Part 1 ------------ #
    start = time()
    password_1 = ''
    index = count()

    while len(password_1) < 8:
        test = get_hash(input_string, next(index))
        if test.startswith('00000'):
            password_1 += test[5]

    print(f'Part 1 password: {password_1}')
    print(f"Time: {time() - start:.2f}s")

    # ------------ Part 2 ------------ #
    start = time()
    password_2 = [None] * 8
    index = count()

    while None in password_2:
        test = get_hash(input_string, next(index))
        if test.startswith('00000') and (pos := int(test[5], 16)) < 8:
            if password_2[pos] is None:
                password_2[pos] = test[6]

    print(f'Part 2 password: {"".join(password_2)}')
    print(f"Time: {time() - start:.2f}s")