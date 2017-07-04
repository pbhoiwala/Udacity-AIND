assignments = []
import itertools

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #Find all instances of naked twins
    #Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        double_set = set() # contains a set of all box values
        twin_set = set()  # contains a set of only the boxes that have 2 possible values

        for box in unit: # loop over each box in the unit and populate the twin_set
            if len(values[box]) == 2: # check if the box has exactly 2 possible values
                if values[box] in double_set:
                    if values[box] in twin_set:        # if value is already there in twin_set, then remove it
                        twin_set.remove(values[box])
                    else:
                        twin_set.add(values[box])      # only add to twin_set if value appears twice
                    double_set.remove(values[box])
                double_set.add(values[box])

        # loop over all the twin_sets
        # compare each twin set with each box (except the twin box i.e don't compare a twin with itself)
        # if any value(s) in twin_set matches in box
        # then remove that value
        for twin in twin_set:
            for box in unit:
                if twin != values[box]:
                    for s in twin:
                        if s in values[box]:
                            #print("naked -> twin=" + twin + " and boxVal=" + values[box] + " and val=" + values[box].replace(s, ''))
                            values = assign_value(values, box, values[box].replace(s, ''))

    return values



def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s + t for s in a for t in b]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[i] + cols[i] for i in range(len(rows))], [rows[::-1][i] + cols[i] for i in range(len(rows))]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    for i in grid:
        val = i if i.isdigit() else '123456789'
        values.append(val)
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    givenBoxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in givenBoxes:
        boxValue = values[box]
        for peer in peers[box]:
            ###values[peer] = values[peer].replace(boxValue, '')
            value = values[peer].replace(boxValue, '')
            values = assign_value(values, peer, value)
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                ###values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])


        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    if values == False: return False
    all = [1 for box in boxes if len(values[box]) == 1]
    if len(all) == 81: return values

    # Choose one of the unfilled squares with the fewest possibilities
    # Copied from solution
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_values = values.copy()
        new_values[s] = value
        sol = search(new_values)
        if sol: return sol

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
