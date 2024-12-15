from pyArango.connection import *
from pyArango.collection import Collection, Field, Edges

# Set up the database connection and collections
conn = Connection(username="root", password="root")
db_name = "magical_square"

if db_name not in conn:
    db = conn.createDatabase(name=db_name)
else:
    db = conn[db_name]


# Define the Nodes and Edges collections
class Nodes(Collection):
    _fields = {"hash": Field()}


class Edges(Edges):
    _fields = {"from_index": Field(), "to_index": Field()}


if "Nodes" not in db.collections:
    db.createCollection(name="Nodes", className="Nodes")
if "Edges" not in db.collections:
    db.createCollection(name="Edges", className="Edges")

nodes = db["Nodes"]
edges = db["Edges"]

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

loosing_hashtable = {}
winning_hashtable = {}
nb_solutions = 0


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
        move = str(squares.get(index)) or "0"

        if len(move) == 1:
            move = "  " + move
        elif len(move) == 2:
            move = " " + move
        str_grid += " " + move + " "

        if index % WIDTH == WIDTH - 1:
            str_grid += "\n"

    return str_grid


def get_moves(grid: int, index: int) -> list[int]:
    indexes = []

    sub_grid_filled = is_sub_grid_filled(grid, index)

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
        if (
            index + HORIZONTAL_OFFSET < DIGITS_NUMBER
            and index % WIDTH < 7
            and not grid & 1 << (index + HORIZONTAL_OFFSET)
        ):
            indexes.append(index + HORIZONTAL_OFFSET)
        if (
            index - HORIZONTAL_OFFSET >= 0
            and index % WIDTH > 2
            and not grid & 1 << (index - HORIZONTAL_OFFSET)
        ):
            indexes.append(index - HORIZONTAL_OFFSET)
        if index + VERTICAL_OFFSET < DIGITS_NUMBER and not grid & 1 << (
            index + VERTICAL_OFFSET
        ):
            indexes.append(index + VERTICAL_OFFSET)
        if index - VERTICAL_OFFSET >= 0 and not grid & 1 << (index - VERTICAL_OFFSET):
            indexes.append(index - VERTICAL_OFFSET)

    return indexes


def solve(grid: int, index: int, played_moves: list[int]) -> bool:
    global loosing_hashtable, winning_hashtable, solutions, nb_solutions
    is_winning = False
    previous_hash = get_hash(grid, index)

    moves = get_moves(grid, index)
    for move in moves:
        grid |= 1 << move
        played_moves.append(move)
        hash = get_hash(grid, move)

        if len(played_moves) == DIGITS_NUMBER:
            is_winning = True
            played_moves.pop(-1)
            grid ^= 1 << move
            continue

        # if we know it's loosing we just skip it
        if loosing_hashtable.get(hash):
            played_moves.pop(-1)
            grid ^= 1 << move
            continue

        # if we already have that pos we just make the link
        if winning_hashtable.get(hash):
            edge_doc = edges.createDocument(
                {
                    "_from": f"Nodes/{str(previous_hash)}",
                    "_to": f"Nodes/{str(hash)}",
                    "from_index": index,
                    "to_index": move,
                }
            )
            edge_doc.save()
            played_moves.pop(-1)
            grid ^= 1 << move
            is_winning = True
            continue

        # if we find it's loosing we just save it as loosing
        if not solve(grid, move, played_moves):
            played_moves.pop(-1)
            grid ^= 1 << move
            loosing_hashtable[hash] = True
            continue

        # if we discover it's winning we create the grid node and the edge with the previous one
        is_winning = True
        winning_hashtable[hash] = True
        edge_doc = edges.createDocument(
            {
                "_from": f"Nodes/{str(previous_hash)}",
                "_to": f"Nodes/{str(hash)}",
                "from_index": index,
                "to_index": move,
            }
        )
        edge_doc.save()

        played_moves.pop(-1)
        grid ^= 1 << move

    if is_winning:
        node_doc = nodes.createDocument(
            {"_key": str(previous_hash), "hash": str(previous_hash)}
        )
        node_doc.save()
    return is_winning


if __name__ == "__main__":
    solve(1, 0, [0])
