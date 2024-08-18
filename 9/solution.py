'''
Part 1:
The compressed form of a string uses interpolated markers of form '(MxN)',
meaning that the next M characters are repeated N times in the original text.
If a marker sequence falls into the data referenced by a previous marker, it
is treated as simple data, e.g. (5x2)(2x2)A --> (2x2)(2x2)A 
We're asked to find the length of the decompressed string.

Part 2:
Now markers that lie in the data referenced by a previous marker must be also
decompressed. Once again, we must find the length of the decompressed string.
'''

import re

# Pattern '(MxN)'. M, N are integers and we capture them in groups
pattern = re.compile(r'\((\d+)x(\d+)\)')

# --------- Part 1 ---------- #

with open('input.txt') as f:
    text = f.read().strip()

# We start off with length equal to that of the compressed string
# and will go on to calculate length adjustments as we scan it
count = len(text)

# Position in string to start scanning from
pos = 0

while True:
    mark = pattern.search(text, pos)
    if not mark:
        break
    m, n = int(mark.group(1)), int(mark.group(2))
    start, end = mark.start(), mark.end()
    # Length adjustment is: M(N-1) - marker_length
    count += m * (n - 1) - (end - start)
    # And we resume scanning M positions after the marker's end
    pos = end + m 
print(count)


# --------- Part 2 ---------- #

def decompress(text):
    if not pattern.search(text):
        return len(text)
    ret = 0
    while pattern.search(text):
        mark = pattern.search(text)
        m, n = int(mark.group(1)), int(mark.group(2))
        # Add number of characters before marker
        ret += mark.start()
        # Update text to begin at position after marker,
        # we've counted everything to this point
        text = text[mark.end():]
        # We make a copy of the next M characters, referenced
        # by current marker, and call the function on that string.
        # This will give us the decompressed length of this chunk
        # which we multiply by N to add to the aggregate length.
        ret += decompress(text[:m]) * n
        # We can then start scanning M positions further, as we've
        # decompressed and calculated everything thus far.
        text = text[m:]
    return ret
    
with open('input.txt') as f:
    text = f.read().strip()

print(decompress(text))