#include <stdio.h>
#include <stdlib.h>

#define WIDTH 10
#define HEIGHT 10
#define DIGITS_NUMBER 100
#define HORIZONTAL_OFFSET 3
#define VERTICAL_OFFSET 30
#define Y_DIAGONAL_OFFSET 20
#define X_DIAGONAL_OFFSET 2
#define TO_RIGHT_OFFSET HORIZONTAL_OFFSET
#define TO_LEFT_OFFSET -HORIZONTAL_OFFSET
#define TO_BOTTOM_OFFSET VERTICAL_OFFSET
#define TO_TOP_OFFSET -VERTICAL_OFFSET
#define TO_BOTTOM_RIGHT_OFFSET Y_DIAGONAL_OFFSET + X_DIAGONAL_OFFSET
#define TO_BOTTOM_LEFT_OFFSET Y_DIAGONAL_OFFSET - X_DIAGONAL_OFFSET
#define TO_TOP_RIGHT_OFFSET -Y_DIAGONAL_OFFSET + X_DIAGONAL_OFFSET
#define TO_TOP_LEFT_OFFSET -Y_DIAGONAL_OFFSET - X_DIAGONAL_OFFSET

//TODO switch from int (4 bytes) to something that take up to 100 bits
char is_subgrid_horizontal_line_filled(int grid, int index){
  int y_offset = index - index % WIDTH;
  int default_x_offset = index % WIDTH % HORIZONTAL_OFFSET;

  for (int x_offset;x_offset<WIDTH;x_offset+=HORIZONTAL_OFFSET){
    if (!(grid & 1 << (y_offset + x_offset))){
      return 0;
    }
  }

  return 1;
}

char is_sub_grid_filled(int grid, int index){
  index %= VERTICAL_OFFSET;
  while (index < DIGITS_NUMBER){
    if (!is_subgrid_horizontal_line_filled(grid, index)){
      return 0;
    }
    index += VERTICAL_OFFSET;
  }

  return 1;
}

int main(){
  return 0;
}
