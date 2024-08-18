'''
In a tile floor arranged in rows of fixed length, some tiles are traps ("^")
and the rest are safe ("."). Given the tile status of the first row, whether
a tile in any row below that is safe is determined by given rules about the
values of the three tiles just above it (left up, center up, right up).
We're asked to count the safe tiles for 40 and for 400000 rows. 
'''

def getValue(pattern):
    return "^" if pattern in ("^^.", ".^^", "^..", "..^") else "."

with open("input.txt") as f:
    first = "." + f.read().strip() + "."
    
def getSafeCount(numRows, previous):
    safeCount = previous.count(".") - 2
    for _ in range(1,numRows):
        row = "."
        for col in range(1, len(previous) -1):
            row += getValue(previous[col-1:col+2])
        row += "."
        safeCount += row.count(".") - 2
        previous = row
    return safeCount

print(f"Part 1: {getSafeCount(40, first)} safe tiles in 40 first rows.")
print(f"Part 2: {getSafeCount(400000, first)} safe tiles in 400000 first rows.")
