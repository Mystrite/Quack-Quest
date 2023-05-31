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

############ VALUE PRESETS BEGIN ############

TILE_ID = {
    "FLOOR": 0,
    "LAVA": 1,
    "HOLY": 2,
    "ROCK": 3,
    "N_VOID": 4,
    "P_VOID": 5,
    "EXIT": 6,
    "ENTER": 7,
    "NONE": 8,
    "O_WALL": 9
}

SIZE_X = 18
SIZE_Y = 8
prob_matrix = [
   # FLOOR      LAVA        HOLY        ROCK        N_VOID      P_VOID  EXIT    ENTER   NONE    O_WALL     
    [0.70,      0.1,        0.005,      0.14,       0.028,      0,      0,      0,      0,      0],         # FLOOR
    [0.50,      0.45,       0,          0.05,       0,          0,      0,      0,      0,      0],         # LAVA
    [0.65,      0,          0.3,        0.05,       0,          0,      0,      0,      0,      0],         # HOLY
    [0.75,      0.10,       0.05,       0.05,       0.05,       0,      0,      0,      0,      0],         # ROCK
    [0.70,      0,          0.005,      0.005,      0.2,        0,      0,      0,      0,      0],         # N_VOID
    [0.70,      0,          0,          0,          0.3,        0,      0,      0,      0,      0],         # P_VOID
    [1,         0,          0,          0,          0,          0,      0,      0,      0,      0],         # EXIT
    [1,         0,          0,          0,          0,          0,      0,      0,      0,      0],         # ENTRANCE
    [0.90,      0.03,       0.005,      0.04,       0.025,      0,      0,      0,      0,      0],         # NONE
    [0,         0,          0,          0,          0,          0,      0,      0,      0,      0]          # O_WALL
    ]

############ VALUE PRESETS END ############

############ GENERAL FUNCS BEGIN ############

def outgrid(grid, width, height):       #output a given 2D array
    for y in range(height):
        outstr = ""
        for x in range(width):
            outstr += str(grid[y][x])
        print(outstr)

############ GENERAL FUNCS END ############

############ MAP GEN FUNCS BEGIN ############
def init_grid(xlen, ylen):      #create 2d array which holds map tiles
    exit_index = r.randint(1,SIZE_X-2)
    enter_index = r.randint(1,SIZE_X-2)
    maptiles = [[TILE_ID["NONE"]] * xlen for i in range(ylen)]
    for x in range(xlen):
        for y in range(ylen):
            if y == 0 and x == exit_index:
                maptiles[0][exit_index] = TILE_ID["EXIT"]
            elif y == ylen-1 and x == enter_index:
                maptiles[y][enter_index] = TILE_ID["ENTER"]
                maptiles[y-1][enter_index] = TILE_ID["FLOOR"]       # ensures entrance is not blocked by a non-floor tile
            elif (y == 0 or y == ylen-1) or (x == 0 or x == xlen-1):
                maptiles[y][x] = TILE_ID["O_WALL"]
    return maptiles, exit_index


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
    outgrid(grid, SIZE_X, SIZE_Y)

    if (x < SIZE_X and y < SIZE_Y and x >= 0 and y >= 0):
       if (grid[y][x] == TILE_ID["NONE"]):  # mostly generates horizontally, not a huge fan
        # generate tile
           newID = rand_select(prob_matrix, ID)
           grid[y][x] = newID
           grid = populate_grid(grid,x+1, y, newID)
           grid = populate_grid(grid,x, y+1, newID)
           grid = populate_grid(grid,x-1, y, newID)
           grid = populate_grid(grid,x, y-1, newID)

       elif grid[y][x] == TILE_ID["EXIT"]:      # ensure that exit is not directly blocked by non-floor tile
           newID = TILE_ID["FLOOR"]
           grid[y-1][x] = newID
           grid = populate_grid(grid,x, y+1, newID)
           grid = populate_grid(grid,x+1, y, newID)
           grid = populate_grid(grid,x-1, y, newID)
           grid = populate_grid(grid,x, y-1, newID)

    return grid

############ MAP GEN FUNCS END ############

def main():
    global maptiles
    global SIZE_X
    global SIZE_Y
    global prob_matrix

    maptiles, n_index = init_grid(SIZE_X, SIZE_Y)        # to be rewritten, mostly output test
    outgrid(maptiles, SIZE_X, SIZE_Y)             
    newgrid = populate_grid(maptiles, n_index, 0, 8)
    print()
    outgrid(newgrid, SIZE_X, SIZE_Y)

main()

