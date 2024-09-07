WIDTH = 10
HEIGHT = 10
DIGITS_NUMBER = 100
HORIZONTAL_DISTANCE = 3
VERTICAL_DISTANCE = WIDTH * HORIZONTAL_DISTANCE
TOPLEFT_BOTTOMRIGHT = 2 + 2 * HORIZONTAL_DISTANCE
BOTTOMLEFT_TOPRIGHT = 2 - 2 * HORIZONTAL_DISTANCE

def is_valid_index(index:int)->bool:
    if index < 0:return False
    if index >= DIGITS_NUMBER:return False
    return True

def get_moves(grid:list[int], index:int)->list[int]:
    indexes = [
        index+HORIZONTAL_DISTANCE,
        index-HORIZONTAL_DISTANCE,
        index+VERTICAL_DISTANCE,
        index-VERTICAL_DISTANCE,
        index+TOPLEFT_BOTTOMRIGHT,
        index-TOPLEFT_BOTTOMRIGHT,
        index+BOTTOMLEFT_TOPRIGHT,
        index-BOTTOMLEFT_TOPRIGHT,
    ]
    indexes = filter(lambda x: is_valid_index(x) and not grid[x], indexes)
    return [index for index in indexes]
    


if __name__ == "__main__":
    grid = [0 for i in range(DIGITS_NUMBER)]
    print(get_moves(grid, 0))
