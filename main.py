WIDTH = 10
HEIGHT = 10
DIGITS_NUMBER = 100
HORIZONTAL_DISTANCE = 3
VERTICAL_DISTANCE = WIDTH * HORIZONTAL_DISTANCE
TOPLEFT_BOTTOMRIGHT = 2 + 2 * WIDTH
BOTTOMLEFT_TOPRIGHT = 2 - 2 * WIDTH

def is_valid_index(index:int)->bool:
    if index < 0:return False
    if index >= DIGITS_NUMBER:return False
    return True

def show_grid(grid:list[int]):
    for i in range(HEIGHT):
        str_line = ""
        for j in range(WIDTH):
            letter = str(grid[i*WIDTH + j])
            if len(letter) == 1:letter = "  " + letter
            elif len(letter) == 2:letter = " " + letter
            str_line += " " + letter + " "
        print(str_line)

def get_moves(grid:list[int], index:int)->list[int]:
    indexes = [
        (index+HORIZONTAL_DISTANCE, lambda x: x%WIDTH < 7),
        (index-HORIZONTAL_DISTANCE, lambda x: x%WIDTH > 2),
        (index+VERTICAL_DISTANCE, lambda x: True),
        (index-VERTICAL_DISTANCE, lambda x: True),
        (index+TOPLEFT_BOTTOMRIGHT, lambda x: x%WIDTH < 8),
        (index-TOPLEFT_BOTTOMRIGHT, lambda x: x%WIDTH > 1),
        (index+BOTTOMLEFT_TOPRIGHT, lambda x: x%WIDTH < 8),
        (index-BOTTOMLEFT_TOPRIGHT, lambda x: x%WIDTH > 1),
    ]
    indexes = filter(lambda x: is_valid_index(x[0]) and x[1](index) and not grid[x[0]], indexes)
    return [index[0] for index in indexes]
    
def dfs(grid:list[int], index:int, depth:int=2)->bool:
    print(depth)

    if depth == 101:
        show_grid(grid)
        return True

    for move in get_moves(grid, index):
        grid[move] = depth

        result = dfs(grid, move, depth+1)
        if result:return True

        grid[move] = 0

    return False


if __name__ == "__main__":
    grid = [0 for i in range(DIGITS_NUMBER)]
    index = 0
    grid[index] = 1
    dfs(grid, 0)
