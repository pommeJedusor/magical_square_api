# Magical Square

## The problem to solve
the problem I'm trying to solve is this one

on a grid 10x10

we put a '1' in the first square (top-left)

then we need to put the following number, the '2'

and then the fun begin we can only place it three squares sooner or later vertically or horizontally

example on a 4x4 grid ('1' for the first digit, '2' for the available squares for the '2', 'x', for the empty squares):
```
1 x x 2
x x x x
x x x x
2 x x x
```

other example:
```
x x x 2
x x x x
x x x x
2 x x 1
```

we can also place the '2' in diagonal with a distance of two this time
example on a 5x5 grid:
```
2 x x x 2
x x x x x
x x 1 x x
x x x x x
2 x x x 2
```

we should then continue like that until we put the number '100' and we complete the 10x10 grid
