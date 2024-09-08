WIDTH = 10
HEIGHT = 10
DIGITS_NUMBER = 100
HORIZONTAL_DISTANCE = 3
VERTICAL_DISTANCE = WIDTH * HORIZONTAL_DISTANCE
TOPLEFT_BOTTOMRIGHT = 2 + 2 * WIDTH
BOTTOMLEFT_TOPRIGHT = 2 - 2 * WIDTH

max_depth = 0
loosing_hashtable = {}

def is_subgrid_horizontal_line_filled(grid:int, index:int)->bool:
    y = index - index % WIDTH
    x = (index % WIDTH % HORIZONTAL_DISTANCE)
    while x < WIDTH:
        if not grid & 1 << (y+x):
            return False
        x += HORIZONTAL_DISTANCE

    return True

def is_sub_grid_filled(grid:int, index:int)->bool:
    index %= VERTICAL_DISTANCE
    while (index < DIGITS_NUMBER):
        if not is_subgrid_horizontal_line_filled(grid, index):
            return False
        index += VERTICAL_DISTANCE
        
    return True

def get_hash(grid:int, index:int)->int:
    return grid | index << 100

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

def get_moves(grid:int, index:int, unperfect=False)->list[int]:
    indexes = []
    if unperfect:sub_grid_filled = is_sub_grid_filled(grid, index)

    if not unperfect or not sub_grid_filled:
        if index+HORIZONTAL_DISTANCE < DIGITS_NUMBER and index%WIDTH < 7 and not grid & 1 << (index+HORIZONTAL_DISTANCE):
            indexes.append(index+HORIZONTAL_DISTANCE)
        if index-HORIZONTAL_DISTANCE >= 0 and index%WIDTH > 2 and not grid & 1 << (index-HORIZONTAL_DISTANCE):
            indexes.append(index-HORIZONTAL_DISTANCE)
        if index+VERTICAL_DISTANCE < DIGITS_NUMBER and not grid & 1 << (index+VERTICAL_DISTANCE):
            indexes.append(index+VERTICAL_DISTANCE)
        if index-VERTICAL_DISTANCE >= 0 and not grid & 1 << (index-VERTICAL_DISTANCE):
            indexes.append(index-VERTICAL_DISTANCE)
    if not unperfect or sub_grid_filled:
        if index+TOPLEFT_BOTTOMRIGHT < DIGITS_NUMBER and index%WIDTH < 8 and not grid & 1 << (index+TOPLEFT_BOTTOMRIGHT):
            indexes.append(index+TOPLEFT_BOTTOMRIGHT)
        if index-TOPLEFT_BOTTOMRIGHT >= 0 and index%WIDTH > 1 and not grid & 1 << (index-TOPLEFT_BOTTOMRIGHT):
            indexes.append(index-TOPLEFT_BOTTOMRIGHT)
        if index+BOTTOMLEFT_TOPRIGHT >= 0 and index%WIDTH < 8 and not grid & 1 << (index+BOTTOMLEFT_TOPRIGHT):
            indexes.append(index+BOTTOMLEFT_TOPRIGHT)
        if index-BOTTOMLEFT_TOPRIGHT < DIGITS_NUMBER and index%WIDTH > 1 and not grid & 1 << (index-BOTTOMLEFT_TOPRIGHT):
            indexes.append(index-BOTTOMLEFT_TOPRIGHT)

    return indexes
    
def dfs(grid:int, index:int, all_moves:list[str], depth:int=2)->bool:
    global max_depth, loosing_hashtable

    if depth > max_depth:
        max_depth = depth
        print(max_depth)
        show_grid(all_moves)

    if depth == 100 + 1:
        show_grid(all_moves)
        return True

    for move in get_moves(grid, index, unperfect=True):
        grid |= 1 << move
        all_moves.append(str(move))

        if not loosing_hashtable.get(get_hash(grid, move)) and (depth > 97 or is_position_valid(grid, move)):
            result = dfs(grid, move, all_moves, depth+1)
            if result:return True

        # save the position as loosing
        loosing_hashtable[get_hash(grid, move)] = (grid, move)

        all_moves.pop(-1)
        grid ^= 1 << move

    return False


if __name__ == "__main__":
    dfs(1, 0, ["0"])
