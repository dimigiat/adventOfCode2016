'''
Given an unsorted list of (possibly overlapping) blacklisted IP blocks,
where IPs are in their integer form (0 - 4294967295), we're asked to find
the first non-blacklisted IP and the number of all non-blacklisted IPs.
'''
    
MAXIP = 4294967295


def get_lowest_free(sorted_list: list[tuple[int, int]]) -> int|None:
    '''
    Given a sorted list of blacklisted blocks of integers, return the lowest
    non-blacklisted integer in 0-MAXIP, or None if all are blacklisted.
    '''
    right_end = -1

    for block in sorted_list:
        if block[0] > right_end + 1:
            return right_end + 1
        right_end = max(right_end, block[1])

    return right_end + 1 if (right_end + 1) <= MAXIP else None


def free_ip_count(sorted_list: list[tuple[int, int]]) -> int:
    '''
    Given a sorted list of blacklisted blocks of integers, return the number 
    of non-blacklisted integers in 0-MAXIP.
    '''
    count = 0
    right_end = -1

    for block in sorted_list:
        if block[0] > right_end + 1:
            count += block[0] - right_end - 1
        right_end = max(right_end, block[1])

    if right_end < MAXIP:
        count += MAXIP - right_end
        
    return count


if __name__ == '__main__':

    with open("input.txt") as f:
        # Blacklist IP blocks sorted by increasing start IP
        sorted_list = sorted(tuple(map(int, line.split("-"))) for line in f)

    print(f"Lowest non-blacklisted IP is {get_lowest_free(sorted_list)}")
    print(f"Number of non-blacklisted IPs: {free_ip_count(sorted_list)}")