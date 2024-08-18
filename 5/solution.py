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

# Using the b'...' bytes literal, which uses ASCII to encode the string, 
# since input only consists of such characters, even after appending index   
input = b'ffykfhsq'

# ---- Part 1 ---- #

start = time()
password_1 = ''
index = count()

while len(password_1) < 8:
    # Byte representation of ASCII characters (including number characters)
    # remains identical under UTF8, so we can use 'ascii' or 'utf8' below
    test_hash = md5(input + bytes(str(next(index)),'utf8')).hexdigest()
    if test_hash.startswith('00000'):
        password_1 += test_hash[5]

print(f"Part 1 password: {password_1}")
print(time() - start)

# ---- Part 2 ---- #

start = time()
password_2 = [None] * 8
index = count()

while None in password_2:
    test_hash = md5(input + bytes(str(next(index)),'utf8')).hexdigest()
    if test_hash.startswith('00000'):
        try:
            pos = int(test_hash[5])
            if pos < 8 and password_2[pos]==None:
                password_2[pos] = test_hash[6]
        except ValueError:
            continue
        

print(f"Part 2 password: {''.join(password_2)}")
print(time() - start)