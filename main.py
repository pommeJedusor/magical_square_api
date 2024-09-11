WIDTH = 10
HEIGHT = 10
DIGITS_NUMBER = 100
HORIZONTAL_OFFSET = 3
VERTICAL_OFFSET = 30
Y_DIAGONAL_OFFSET = 20
X_DIAGONAL_OFFSET = 2
TO_RIGHT_OFFSET = HORIZONTAL_OFFSET
TO_LEFT_OFFSET = -HORIZONTAL_OFFSET
TO_BOTTOM_OFFSET = VERTICAL_OFFSET
TO_TOP_OFFSET = -VERTICAL_OFFSET
TO_BOTTOM_RIGHT_OFFSET = Y_DIAGONAL_OFFSET + X_DIAGONAL_OFFSET
TO_BOTTOM_LEFT_OFFSET = Y_DIAGONAL_OFFSET - X_DIAGONAL_OFFSET
TO_TOP_RIGHT_OFFSET = -Y_DIAGONAL_OFFSET + X_DIAGONAL_OFFSET
TO_TOP_LEFT_OFFSET = -Y_DIAGONAL_OFFSET - X_DIAGONAL_OFFSET

max_depth = 0
loosing_hashtable = {}
solutions = []


def is_subgrid_horizontal_line_filled(grid: int, index: int) -> bool:
    y = index - index % WIDTH
    x = index % WIDTH % HORIZONTAL_OFFSET
    while x < WIDTH:
        if not grid & 1 << (y + x):
            return False
        x += HORIZONTAL_OFFSET

    return True


def is_sub_grid_filled(grid: int, index: int) -> bool:
    index %= VERTICAL_OFFSET
    while index < DIGITS_NUMBER:
        if not is_subgrid_horizontal_line_filled(grid, index):
            return False
        index += VERTICAL_OFFSET

    return True


def get_hash(grid: int, index: int) -> int:
    return grid | index << 100


def show_grid(played_moves: list[str]) -> str:
    positions = {}
    for i in range(len(played_moves)):
        positions[played_moves[i]] = str(i + 1)

    str_grid = ""
    for i in range(HEIGHT):
        str_line = ""
        for j in range(WIDTH):
            move = positions.get(str(i * WIDTH + j)) or "0"
            if len(move) == 1:
                move = "  " + move
            elif len(move) == 2:
                move = " " + move
            str_line += " " + move + " "
        str_grid += str_line + "\n"
    return str_grid


def get_moves(grid: int, index: int, unperfect=False) -> list[int]:
    indexes = []

    sub_grid_filled = not unperfect or is_sub_grid_filled(grid, index)

    if not unperfect or not sub_grid_filled:
        # right
        if (
            index + HORIZONTAL_OFFSET < DIGITS_NUMBER
            and index % WIDTH < 7
            and not grid & 1 << (index + HORIZONTAL_OFFSET)
        ):
            indexes.append(index + HORIZONTAL_OFFSET)
        # left
        if (
            index - HORIZONTAL_OFFSET >= 0
            and index % WIDTH > 2
            and not grid & 1 << (index - HORIZONTAL_OFFSET)
        ):
            indexes.append(index - HORIZONTAL_OFFSET)
        # down
        if index + VERTICAL_OFFSET < DIGITS_NUMBER and not grid & 1 << (
            index + VERTICAL_OFFSET
        ):
            indexes.append(index + VERTICAL_OFFSET)
        # up
        if index - VERTICAL_OFFSET >= 0 and not grid & 1 << (index - VERTICAL_OFFSET):
            indexes.append(index - VERTICAL_OFFSET)
    if not unperfect or sub_grid_filled:
        if (
            index + TO_BOTTOM_RIGHT_OFFSET < DIGITS_NUMBER
            and index % WIDTH < 8
            and not grid & 1 << (index + TO_BOTTOM_RIGHT_OFFSET)
        ):
            indexes.append(index + TO_BOTTOM_RIGHT_OFFSET)
        if (
            index - TO_BOTTOM_RIGHT_OFFSET >= 0
            and index % WIDTH > 1
            and not grid & 1 << (index - TO_BOTTOM_RIGHT_OFFSET)
        ):
            indexes.append(index - TO_BOTTOM_RIGHT_OFFSET)
        if (
            index + TO_TOP_RIGHT_OFFSET >= 0
            and index % WIDTH < 8
            and not grid & 1 << (index + TO_TOP_RIGHT_OFFSET)
        ):
            indexes.append(index + TO_TOP_RIGHT_OFFSET)
        if (
            index - TO_TOP_RIGHT_OFFSET < DIGITS_NUMBER
            and index % WIDTH > 1
            and not grid & 1 << (index - TO_TOP_RIGHT_OFFSET)
        ):
            indexes.append(index - TO_TOP_RIGHT_OFFSET)

    return indexes


def dfs(grid: int, index: int, played_moves: list[str], depth: int = 2) -> bool:
    global max_depth, loosing_hashtable, solutions

    if depth == 100 + 1:
        solutions.append(played_moves.copy())
        return True

    for move in get_moves(grid, index, unperfect=True):
        grid |= 1 << move
        played_moves.append(str(move))

        result = False
        if not loosing_hashtable.get(get_hash(grid, move)):
            result = dfs(grid, move, played_moves, depth + 1)

        # save the position as loosing
        if not result:
            loosing_hashtable[get_hash(grid, move)] = (grid, move)

        played_moves.pop(-1)
        grid ^= 1 << move

    return False


if __name__ == "__main__":
    dfs(1, 0, ["0"])
    text = f"-- all solutions ({len(solutions)}) --\n"
    for i in range(len(solutions)):
        text += f"# solution {i+1}:\n"
        text += show_grid(solutions[i])
    print(text)
    with open("./solutions.txt", "w", encoding="utf8") as f:
        f.write(text)
