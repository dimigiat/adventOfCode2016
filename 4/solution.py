'''
Part 1:
Given a list of strings consisting of lowercase letters separated by dashes,
a 3-digit numeric sector ID and a 5-letter checksum (in square brackets) are 
appended to each string (example: 'enzcntvat-pnaql-qrfvta-351[antqv]')
A correct checksum must consist of the string's five most common letters
in order of decreasing frequency, ties broken alphabetically.
Target is to find the sum of the IDs of the valid strings.

Part 2:
The valid strings are encrypted. To decrypt each string, we have to rotate
each letter forward through the alphabet as many times as its sector ID.
The dashes become spaces. Target is to find sector ID of room with the
decrypted name "northpole object storage".
'''

from collections import Counter

id_aggr = 0

def rotate_char(s, shift):
    '''
    Shift all characters of string by shift characters, staying
    within lowercase ASCII (i.e. ... y -> z -> a -> b ...)
    '''
    if not isinstance(s, str) or not isinstance(shift, int): 
        raise TypeError
    shifted = [chr( (ord(c) - ord('a') + shift) % 26 + ord('a') ) 
               if c!='-' else ' ' for c in s]
    return ''.join(shifted)

with open('input.txt') as data:
    for room in data:
        encr = room.strip()[:-11]
        letters = ''.join(sorted(encr)).lstrip('-')
        sid = int(room.strip()[-10:-7])
        cks = room.strip()[-6:-1]
        # Since letters are sorted, ties in Counter are broken alphabetically
        if cks == ''.join([c for c,v in Counter(letters).most_common(5)]):
            id_aggr += sid
            if rotate_char(encr, sid) == "northpole object storage":
                print(f"Sector ID of target room: {sid}")

print(f"Sector ID sum of valid room entries: {id_aggr}")