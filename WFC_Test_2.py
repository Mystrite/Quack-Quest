"""
TILE ID:
0 - None
1 - Floor
2 - Lava
3 - Holy Water
4 - Rock
5 - New Void
6 - Pre-set Void
7 - Exit
8 - Entrance
"""

import random as r

TILE_ID = {
    "FLOOR": 0,
    "LAVA": 1,
    "HOLY": 2,
    "ROCK": 3,
    "N_VOID": 4,
    "P_VOID": 5,
    "EXIT": 6,
    "ENTER": 7,
    "NONE": 8
}

SIZE_X = 18
SIZE_Y = 8
prob_matrix = [
   # FLOOR      LAVA        HOLY        ROCK        N_VOID      P_VOID  EXIT    ENTER   NONE     
    [0.90,      0.03,       0.005,      0.04,       0.025,      0,      0,      0,      0],     # FLOOR
    [0.50,      0.4,        0,          0.07,       0.03,       0,      0,      0,      0],     # LAVA
    [0.65,      0,          0.3,        0.05,       0,          0,      0,      0,      0],     # HOLY
    [0.75,      0.10,       0.05,       0.05,       0.05,       0,      0,      0,      0],     # ROCK
    [0.80,      0,          0.005,      0.005,      0.1,        0,      0,      0,      0],     # N_VOID
    [0.70,      0,          0,          0,          0.3,        0,      0,      0,      0],     # P_VOID
    [0,         0,          0,          0,          0,          0,      0,      0,      0],     # EXIT
    [0,         0,          0,          0,          0,          0,      0,      0,      0],     # ENTRANCE
    [0.90,      0.03,       0.005,      0.04,       0.025,      0,      0,      0,      0]      # NONE
    ]

def init_grid(xlen, ylen):      #create 2d array which holds map tiles
    maptiles = [[TILE_ID["NONE"]] * xlen for i in range(ylen)]
    return maptiles

def outgrid(grid, width, height):       #output a given 2D array
    for y in range(height):
        outstr = ""
        for x in range(width):
            outstr += str(grid[y][x])
        print(outstr)

def rand_select(matrix, adj_ID):        #select a tile type, given a tile next to it and a probability matrix
    randnum = r.randint(0,1000) / 1000
    selected = False
    selected_ID = 0
    i = -1
    sum = 0 
    while selected == False and i+1 < len(TILE_ID):
        i += 1
        sum += matrix[adj_ID][i]
        if randnum < sum:
            selected = True
            selected_ID = i
    
    return selected_ID
     
def populate_grid(grid, x, y, ID):      #populate given grid
    if (x < SIZE_X and y < SIZE_Y and x >= 0 and y >= 0) and (grid[y][x] == TILE_ID["NONE"]):
        # generate tile
        newID = rand_select(prob_matrix, ID)
        grid[y][x] = newID
        grid = populate_grid(grid,x+1, y, newID)
        grid = populate_grid(grid,x-1, y, newID)
        grid = populate_grid(grid,x, y+1, newID)
        grid = populate_grid(grid,x, y-1, newID)
    return grid

def main():
    global maptiles
    global SIZE_X
    global SIZE_Y
    global prob_matrix

    maptiles = init_grid(SIZE_X, SIZE_Y)        # to be rewritten, mostly output test
    outgrid(maptiles, SIZE_X, SIZE_Y)             
    newgrid = populate_grid(maptiles, 0, 0, 8)
    print()
    outgrid(newgrid, SIZE_X, SIZE_Y)

main()

