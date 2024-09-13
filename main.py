from db import insert_solutions

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

# store in a dictionnary all the loosing positions
loosing_hashtable = {}
# store for each position the moves available to avoid recomputing them
moves_hashtable = {}
# store in a list all the solutions found
solutions = []
nb_solutions = 0


# a subgrid is of a square 'a' is the set of all the squares that 'a' can go to with only horizontal and vertical moves
# e.g. in normal setting the subgrid of the square of index 0 is composed of the squares of indexes
#  0,  3,  6,  9
# 30, 33, 36, 39
# 60, 63, 66, 69
# 90, 93, 96, 99
def is_subgrid_horizontal_line_filled(grid: int, index: int) -> bool:
    y_offset = index - index % WIDTH
    default_x_offset = index % WIDTH % HORIZONTAL_OFFSET

    for x_offset in range(default_x_offset, WIDTH, HORIZONTAL_OFFSET):
        if not grid & 1 << (y_offset + x_offset):
            return False

    return True


def is_sub_grid_filled(grid: int, index: int) -> bool:
    index %= VERTICAL_OFFSET
    while index < DIGITS_NUMBER:
        if not is_subgrid_horizontal_line_filled(grid, index):
            return False
        index += VERTICAL_OFFSET

    return True


# the position/hash will only be the squares filled and the current index so that a position may be acquired by multiple path
# but the result will be the same
# the index is << of the size of the grid so that they don't superpose
# e.g. on a 2x2 grid with an index of 1
# hash =
#        0010 (grid 0b0010)
#    00010000 (index 1 or 0b0001)
#    00010010 (result)
def get_hash(grid: int, index: int) -> int:
    return grid | index << DIGITS_NUMBER


def show_grid(played_moves: list[int]) -> str:
    # played_moves: turn -> move (index)
    # squares: index -> turn ("1" -> "100")
    squares = {}
    for i in range(len(played_moves)):
        squares[played_moves[i]] = i + 1

    str_grid = ""
    for index in range(DIGITS_NUMBER):
        # get the turn the square has been filled
        move = str(squares.get(index)) or "0"

        # add space so that once the grid is printed, columns align nicely
        if len(move) == 1:
            move = "  " + move
        elif len(move) == 2:
            move = " " + move
        str_grid += " " + move + " "

        # end of the row
        if index % WIDTH == WIDTH - 1:
            str_grid += "\n"

    return str_grid


def get_moves(grid: int, index: int) -> list[int]:
    # all the index that are available to go to
    indexes = []

    sub_grid_filled = is_sub_grid_filled(grid, index)

    # wait until the subgrid is filled to move to the next subgrid
    # it might prune some solutions but it allow to really fastly find a lot of solutions
    # return horizontal and vertical if subgrid not filled and diagonal otherwise
    if sub_grid_filled:
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
    else:
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

    return indexes


def solve(grid: int, index: int, played_moves: list[int]) -> bool:
    global loosing_hashtable, solutions, nb_solutions
    is_winning = False

    # if grid is full
    if len(played_moves) == DIGITS_NUMBER:
        solutions.append(played_moves.copy())
        nb_solutions += 1
        if len(solutions) == 500_000:
            print(nb_solutions)
            print("saving...")
            # insert the current found solutions in db
            insert_solutions(solutions)
            # free the found solutions to free memory space
            solutions = []
            print("save done")
        return True

    # if the moves of the position has already been computed get from hashtable
    moves = moves_hashtable.get(get_hash(grid, index)) or get_moves(grid, index)
    # store the moves in the hashtable
    moves_hashtable[get_hash(grid, index)] = moves
    for move in moves:
        # make the move
        grid |= 1 << move
        played_moves.append(move)

        result = False
        # go deeper if the position doesn't match any previous loosing position explored
        if not loosing_hashtable.get(get_hash(grid, move)):
            result = solve(grid, move, played_moves)

        # save the position as loosing
        if not result:
            loosing_hashtable[get_hash(grid, move)] = True
        else:
            is_winning = True

        # cancel the move
        played_moves.pop(-1)
        grid ^= 1 << move

    return is_winning


if __name__ == "__main__":
    solve(1, 0, [0])
    insert_solutions(solutions)
