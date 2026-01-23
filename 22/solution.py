'''
We are given an MxN storage grid with each node connected to nodes
adjacent to it (4 in the interior, 3 on edges, 2 on corners). 
Our input: the total, used and available storage space per node. 
A valid move consists in moving ALL the data of a node to an adjacent
node, provided the latter has enough available space for it.

For part 1, we must count the viable pairs of nodes, i.e. all pairs 
(A, B), regardless if they're connected, with A being non-empty and 
different from B and whose data fits on B's available space.

For part 2, we need to find the smallest number of total moves for
getting the data of a specified goal node to a specified access node. 

Part 2 seems almost intractable in the general case,
but observing our actual input we see some KEY PROPERTIES:
- Only ONE node is initially EMPTY.
- Among the initially non-empty nodes, the maximum available space 
is less than the minimum data. The only way that a node's data 
could fit into another non-empty node would be for the latter to
be emptied at some point and then receive a data block small enough
to make its available space more than the minimum data. 
We'll see that this is not possible with our input.  
- We partition the nodes in two sets: TOO_LARGE nodes, whose data
exceeds the size of the initially empty node, and REGULAR nodes, 
all others including the initially empty node.
- The minimum data in TOO_LARGE nodes is greater than the size of
any REGULAR node. Thus, data of a TOO_LARGE node can NEVER occupy 
a REGULAR node, even if it's empty. Since they can't be emptied, 
they can't receive data blocks. It follows that TOO_LARGE nodes 
can NEVER take part in any move, we can consider them as WALLS. 
- The maximum size of a REGULAR node is less than twice the minimum
data. Thus, we can NEVER move data between two non-empty REGULAR nodes.
- Given all the above, a move is ALWAYS a swap between the currently 
empty node and an adjacent REGULAR node. Moreover, since among 
REGULAR nodes the minimum size is larger than the maximum data, 
ALL such moves are feasible, so REGULAR nodes are interchangeable.

Due to these properties, tracking the positions of the goal data
and the currently empty node, while excluding wall nodes from the
neighbors of a node, is all we need. A simple BFS until a state
where the goal data occupies the access position is sufficient.

Note that the code works for any input where the node usage stats
satisfy the properties laid out above, not just AoC's 2016 day 22.
'''

import re

from typing import NamedTuple
from collections import deque
from itertools import product

ACCESS_COORDS = (0, 0)
INITIAL_GOAL_COORDS = (29, 0)
X_PATTERN = re.compile(r'x(\d+)')
Y_PATTERN = re.compile(r'y(\d+)')


class Position(NamedTuple):
    x: int
    y: int


class NodeStat(NamedTuple):
    used: int
    avail: int


class State(NamedTuple):
    goal: Position
    empty: Position


def get_grid_from_input(path: str) -> dict[Position, NodeStat]:
    '''
    Parse input file to get a map from (x,y) positions to
    (used, avail) initial node statuses.
    '''
    grid: dict[Position, NodeStat] = {}

    with open(path) as f:
        
        # Skip header lines
        next(f)
        next(f)

        for line in f:
            x = int(X_PATTERN.search(line).group(1))
            y = int(Y_PATTERN.search(line).group(1))
            # Order of usage stats if fixed for output of df.
            # Interpreting units would be an overkill for this problem,
            # we assume all stats share the same unit, here Terabytes (T)
            used, avail = (int(i.rstrip('T')) for i in line.split()[2:4])
            grid[Position(x, y)] = NodeStat(used, avail)

    return grid


def validate_and_get_walls(grid: dict[Position, NodeStat]) -> set[Position]:
    '''
    Validate that all conditions that make the problem tractable,
    as explained in module's docstring, are satisfied.
    If any is violated, throw explanatory exception.
    If not, return the set of unmovable (wall) positions.
    '''
    empty_nodes = [pos for pos, stat in grid.items() if stat.used == 0]

    if len(empty_nodes) != 1:
        raise ValueError('Input must have exactly one empty node.')
    
    initial_empty_pos = empty_nodes[0]
    empty_size = grid[initial_empty_pos].avail

    walls = {
        pos for pos, stat in grid.items()
        if stat.used > empty_size
    }

    min_data = min([stat.used for stat in grid.values() if stat.used > 0])
    max_avail = max([stat.avail for stat in grid.values() if stat.used > 0])

    wall_data = [
        stat.used for pos, stat in grid.items() 
        if pos in walls
    ]

    regular_sizes = [
        sum(stat) for pos, stat in grid.items() 
        if pos not in walls
    ]

    regular_data = [
        stat.used for pos, stat in grid.items() 
        if pos not in walls
    ]

    if min_data <= max_avail:
        raise ValueError(
            'The minimum of used data in non-empty nodes must be '
            'greater than the maximum of available space among them.'
        )

    if len(walls) > 0 and min(wall_data) < max(regular_sizes):
        raise ValueError(
            'If the input has nodes with used data more than the size '
            'of the empty node, then the minimum of those data must '
            'be larger than the maximum size of all other nodes.'
        )

    if max(regular_sizes) >= 2 * min_data:
        raise ValueError(
            'Among nodes whose data is less than the size of the empty '
            'node, the maximum of their sizes must be less than twice '
            'the minimum of used data.'
        )

    if max(regular_data) > min(regular_sizes):
        raise ValueError(
            'Among nodes whose data is less than the size of the empty '
            'node, the maximum of their data must be less than or equal '
            'to the minimum of their sizes, to guarantee interchangeability.'
        )
    
    initial_goal_pos = Position(*INITIAL_GOAL_COORDS)
    access_pos = Position(*ACCESS_COORDS)

    if initial_goal_pos in walls:
        raise ValueError("Goal node is a wall; impossible.")

    if access_pos in walls:
        raise ValueError("Access node is a wall; impossible.")
    
    return walls


def get_empty_pos(grid: dict[Position, NodeStat]) -> Position:
    '''
    Return initial position of empty node.
    '''
    for pos, stat in grid.items():
        if stat.used == 0:
            break
    return pos


def make_neighbor_map(walls: set[Position],
                      xsize: int,
                      ysize: int) -> dict[Position, list[Position]]:
    '''
    Given grid dimensions and positions of walls, 
    return a map from non-wall positions to neighboring positions.
    '''

    def neighbors(pos: Position) -> list[Position]:

        x, y = pos

        nb_candidates = [
            Position(x-1, y), 
            Position(x+1, y), 
            Position(x, y-1), 
            Position(x, y+1)
        ]

        nb_list = [
            nb 
            for nb in nb_candidates
            if nb not in walls
            and nb.x >= 0
            and nb.y >= 0
            and nb.x < xsize
            and nb.y < ysize
        ]

        return nb_list
    
    grid_range = (
        Position(i, j) 
        for i, j in product(range(xsize), range(ysize))
    )

    return {pos: neighbors(pos) for pos in grid_range if pos not in walls}


def next_states(current: State, 
                neighbor_map: dict[Position, list[Position]]) -> list[State]:
    '''
    Given the current state as (goal_pos, empty_pos), 
    we return a list of the possible next states
    '''
    goal_pos, empty_pos = current
    results: list[State] = []

    for nb in neighbor_map[empty_pos]:
        if nb == goal_pos: # swapping goal node with empty node
            results.append(State(empty_pos, nb))
        else: # swapping non-goal node with empty node
            results.append(State(goal_pos, nb))

    return results


def fewest_moves(start_state: State,
                 end_states: set[State],
                 neighbor_map: dict[Position, list[Position]]) -> int|None:
    '''
    With state as (goal_pos, empty_pos), we perform BFS to return the
    minimum number of moves required to bring the goal data from its
    initial position to the access position. 
    
    When goal_pos == access_pos, empty_pos can be any neighbor of 
    access_pos, hence in the general case we have multiple end states.

    If access_pos is not reachable by the goal data given the starting
    state and the neighbor_map, return None.
    '''
    queue = deque([(start_state, 0)]) # each queue item: (state, num_steps)
    visited = set([start_state])

    while queue:
        current, num_steps = queue.popleft()
        if current in end_states:
            return num_steps
        for nxt in next_states(current, neighbor_map):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, num_steps + 1))

    return None


if __name__ == '__main__':

    grid = get_grid_from_input('input.txt')
    xsize = max(pos.x for pos in grid) + 1
    ysize = max(pos.y for pos in grid) + 1

    # Ensure problem is tractable and return set of wall positions
    walls = validate_and_get_walls(grid) 

    initial_empty_pos = get_empty_pos(grid)

    neighbor_map = make_neighbor_map(walls, xsize, ysize)

    initial_goal_pos = Position(*INITIAL_GOAL_COORDS)
    access_pos = Position(*ACCESS_COORDS)
    access_neighbors = neighbor_map[access_pos]

    start_state = State(initial_goal_pos, initial_empty_pos)
    end_states = {State(access_pos, nb) for nb in access_neighbors}

    min_moves = fewest_moves(start_state, end_states, neighbor_map)

    # Viable pairs are those between non-empty REGULAR (non-WALL)
    # nodes and the single empty node: grid_size - num_walls - 1
    print(f'Part 1: {len(grid) - len(walls) - 1} viable pairs.')

    if min_moves is not None:
        print(f'Part 2: Minimum number of moves: {min_moves}.')
    else:
        print('Access node not reachable by goal data via valid moves.')