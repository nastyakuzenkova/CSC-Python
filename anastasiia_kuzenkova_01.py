#python homework^1 task^1
def shape(m):
    #calculate size of matrix
    return len(m), len(m[0])


def print_map(m, pos):
    #print map with free and reserved positions and mark current position
    n_rows, n_cols = shape(m)
    for i in range(n_rows):
        for j in range(n_cols):
            if (i, j) == pos:
                #marked position
                print('@', end = "")
            elif m[i][j]:
                #free position
                print('.', end = "")
            else:
                #reserved position
                print('#', end = "")
        print()


def neighbours(m, pos):
    #find free positions nearby current (top, bottom, left and right)
    answer = []
    pos_row, pos_column = pos
    shifts = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in shifts:
        n_pos = (pos_row + dr, pos_column + dc)
        n_pos_row, n_pos_column = n_pos
        if is_pos_valid(m, n_pos) and m[n_pos_row][n_pos_column]:
            answer.append(n_pos)
    return answer

def is_pos_valid(m, pos):
    #check if current position is inside the map
    pos_row, pos_column = pos
    n_rows, n_cols = shape(m)
    return pos_row >= 0 and pos_row < n_rows and pos_column >= 0 and pos_row < n_rows


def find_route(m, initial):
    #find path from current position to one of the side free positions
    paths = []
    visited = set()
    paths.append([initial])
    while paths:
        path = paths.pop(0)
        node = path[-1]
        visited.add(node)
        if is_exit(m, node):
            return path
        for neighbour in neighbours(m, node):
            if neighbour not in visited:
                next_path = path[:]
                next_path.append(neighbour)
                paths.append(next_path)
    return []


def is_exit(m, initial):
    #check if current position is side position and free
    initial_row, initial_column = initial
    n_rows, n_cols = shape(m)
    return (initial_row == 0 or initial_column == 0 or \
            initial_row == n_rows - 1 or initial_column == n_cols - 1) \
            and m[initial_row][initial_column]


def escape(m, initial):
    #print one of the paths to escape
    route = find_route(m, initial)
    if not route:
        print("there is no path to escape")
        return
    for pos in route:
        print_map(m, pos)
        print()


#python homework^1 task^2
def hamming(seq1, seq2):
    assert len(seq1) == len(seq2)
    length = len(seq1)
    distance = 0
    for i in range(length):
        if seq1[i] != seq2[i]:
            distance += 1
    return distance


def hba1(path, distance):
    sequences = []
    with open(path) as sequences_file:
        sequences = sequences_file.read().splitlines()
    sequences_size = len(sequences)
    hamming_min = len(sequences[0])
    hamming_indexes = (0, 0)
    for i in range(sequences_size):
        for j in range(i + 1, sequences_size):
            hamming_current = distance(sequences[i], sequences[j])
            if hamming_current < hamming_min:
                hamming_min = hamming_current
                hamming_indexes = (i + 1, j + 1)
    return hamming_indexes


#python homework^1 task^3
def kmers(seq, k = 2):
    dictionary = {}
    length = len(seq)
    for i in range(length - k + 1):
        substring = seq[i : i + k]
        if substring not in dictionary:
            dictionary[substring] = 1
        else:
            dictionary[substring] += 1
    return dictionary


def distance1(seq1, seq2, k = 2):
    seq1_dictionary = kmers(seq1, k)
    seq2_dictionary = kmers(seq2, k)
    substrings = set(list(seq1_dictionary.keys()) + list(seq2_dictionary.keys()))
    distance = 0
    for substring in substrings:
        distance += abs(seq1_dictionary.get(substring, 0) - seq2_dictionary.get(substring, 0))
    return distance
