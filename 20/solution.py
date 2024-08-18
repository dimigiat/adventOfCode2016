'''
Given an unsorted list of (possibly overlapping) blacklisted IP blocks,
where IPs are in their integer form (0 - 4294967295), we're asked to find
the first non-blacklisted IP and the number of all non-blacklisted IPs.
'''

with open("input.txt") as f:
    sortedList = sorted(([int(ip) for ip in line.strip().split("-")] 
                         for line in f))
    
MAXIP = 4294967295

def getLowestFree(sortedList):
    rightEnd = -1
    for block in sortedList:
        if block[0] > rightEnd + 1:
            return rightEnd + 1
        rightEnd = max(rightEnd, block[1])
    return rightEnd + 1 if (rightEnd + 1) <= MAXIP else None

def freeIPCount(sortedList):
    count = 0
    rightEnd = -1
    for block in sortedList:
        if block[0] > rightEnd + 1:
            count += block[0] - rightEnd - 1
        rightEnd = max(rightEnd, block[1])
    if rightEnd < MAXIP:
        count += MAXIP - rightEnd
    return count

print(f"Lowest non-blacklisted IP is {getLowestFree(sortedList)}")
print(f"Number of non-blacklisted IPs: {freeIPCount(sortedList)}")