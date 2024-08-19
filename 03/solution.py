'''
Part 1: Given a list of 3-tuples which supposedly describe the
side lengths for a list of triangles, we are asked to count how
many of those satisfy the triangle inequality.
Part 2: Same, but now we read input in columns, thus the side
lengths for each candidate triangle are read three at a time
column-wise, with no correlation between columns.
'''

def is_valid(lengths):
    '''Given an iterable of 3 positive numeric values, return True
    if they satisfy triangle inequality, else return False'''
    return max(lengths) < sum(lengths) - max(lengths)

def line_to_tuple(line):
    return tuple(map(int,line.strip().split()))


# ------------------- Part 1 --------------------- #

with open('input.txt') as data:
    valid_count = sum(map(is_valid, map(line_to_tuple, data)))

print(valid_count)

# ------------------- Part 2 --------------------- #

valid_count = 0

with open('input.txt') as data:
    '''
    [data]*3 gives 3 pointers to the file iterator (cf. grouper recipe).
    Iterating over the zip of this, after mapping lines to tuples,
    gives us a 3-by-3 batch of data at a time, as a tuple of three 
    tuples, for example: ( (5,6,3), (2,4,5), (1,5,2) ). 
    We zip each of those batches to read it column-wise, turning the
    above to: ( (5,2,1), (6,4,5), (3,5,2) ), and check how many of those
    are valid triangles, to update the aggregate valid count.
    '''
    for batch in zip(*[map(line_to_tuple, data)]*3):
        valid_count += sum(map(is_valid, zip(*batch)))
       
print(valid_count)