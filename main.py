WIDTH = 10
HEIGHT = 10
DIGITS_NUMBER = 100
HORIZONTAL_DISTANCE = 3
VERTICAL_DISTANCE = WIDTH * HORIZONTAL_DISTANCE
TOPLEFT_BOTTOMRIGHT = 2 + 2 * WIDTH
BOTTOMLEFT_TOPRIGHT = 2 - 2 * WIDTH

max_depth = 0
loosing_hashtable = {}

def get_hash(grid:int, index:int):
    return grid | 1 << index

def is_dfs_valid(grid:int, last_move:int)->bool:
    zeros = []
    for i in range(DIGITS_NUMBER):
        if not grid & 1 << i:
            zeros.append(i)
    nb_linked = 0
    explored = {}
    unexplored = [zeros[0]]
    while unexplored:
        node = unexplored.pop(-1)
        moves = get_moves(grid, node)
        for move in moves:
            if not explored.get(move):
                unexplored.append(move)
                explored[move] = True
                nb_linked += 1
    return nb_linked == len(zeros)

def is_position_valid(grid:int, last_move:int)->bool:
    moves = get_moves(grid, last_move)
    for move in moves:
        if not get_moves(grid, move):
            return False
    return is_dfs_valid(grid, moves)

def is_valid_index(index:int)->bool:
    if index < 0:return False
    if index >= DIGITS_NUMBER:return False
    return True

def show_grid(all_moves:list[str]):
    positions = {}
    for i in range(len(all_moves)):
        positions[all_moves[i]] = str(i+1)

    for i in range(HEIGHT):
        str_line = ""
        for j in range(WIDTH):
            move = positions.get(str(i * WIDTH + j)) or "0"
            if len(move) == 1:move = "  " + move
            elif len(move) == 2:move = " " + move
            str_line += " " + move + " "
        print(str_line)

def get_moves(grid:int, index:int)->list[int]:
    indexes = []
    if is_valid_index(index+HORIZONTAL_DISTANCE) and index%WIDTH < 7 and not grid & 1 << (index+HORIZONTAL_DISTANCE):
        indexes.append(index+HORIZONTAL_DISTANCE)
    if is_valid_index(index-HORIZONTAL_DISTANCE) and index%WIDTH > 2 and not grid & 1 << (index-HORIZONTAL_DISTANCE):
        indexes.append(index-HORIZONTAL_DISTANCE)
    if is_valid_index(index+VERTICAL_DISTANCE) and not grid & 1 << (index+VERTICAL_DISTANCE):
        indexes.append(index+VERTICAL_DISTANCE)
    if is_valid_index(index-VERTICAL_DISTANCE) and not grid & 1 << (index-VERTICAL_DISTANCE):
        indexes.append(index-VERTICAL_DISTANCE)
    if is_valid_index(index+TOPLEFT_BOTTOMRIGHT) and index%WIDTH < 8 and not grid & 1 << (index+TOPLEFT_BOTTOMRIGHT):
        indexes.append(index+TOPLEFT_BOTTOMRIGHT)
    if is_valid_index(index-TOPLEFT_BOTTOMRIGHT) and index%WIDTH > 1 and not grid & 1 << (index-TOPLEFT_BOTTOMRIGHT):
        indexes.append(index-TOPLEFT_BOTTOMRIGHT)
    if is_valid_index(index+BOTTOMLEFT_TOPRIGHT) and index%WIDTH < 8 and not grid & 1 << (index+BOTTOMLEFT_TOPRIGHT):
        indexes.append(index+BOTTOMLEFT_TOPRIGHT)
    if is_valid_index(index-BOTTOMLEFT_TOPRIGHT) and index%WIDTH > 1 and not grid & 1 << (index-BOTTOMLEFT_TOPRIGHT):
        indexes.append(index-BOTTOMLEFT_TOPRIGHT)
    return indexes
    
def dfs(grid:int, index:int, all_moves:list[str], depth:int=2)->bool:
    global max_depth, loosing_hashtable

    if depth > max_depth:max_depth = depth
    print(depth, max_depth)

    if depth == 96 + 1:
        show_grid(all_moves)
        return True

    for move in get_moves(grid, index):
        grid |= 1 << move
        all_moves.append(str(move))

        if not loosing_hashtable.get(get_hash(grid, move)) and is_position_valid(grid, move):
            result = dfs(grid, move, all_moves, depth+1)
            if result:return True

        # save the position as loosing
        loosing_hashtable[get_hash(grid, move)] = True

        all_moves.pop(-1)
        grid ^= 1 << move

    return False


if __name__ == "__main__":
    grid = 0
    index = 0
    grid |= 1 << index
    all_moves = ["0"]
    dfs(grid, 0, all_moves)
