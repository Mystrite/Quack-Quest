import random as r

############ VALUE PRESETS BEGIN ############

TILE_ID = {
    "FLOOR": 0,
    "LAVA": 1,
    "HOLY": 2,
    "ROCK": 3,
    "VOID": 4,
    "EXIT": 5,
    "ENTER": 6,
    "NONE": 7,
    "O_WALL": 8
}

SIZE_X = 18
SIZE_Y = 8
prob_matrix = [
   # FLOOR      LAVA        HOLY        ROCK        VOID       EXIT    ENTER   NONE    O_WALL     
    [0.7,       0.1,        0.005,      0.14,       0.028,     0,      0,      0,      0],         # FLOOR
    [0.5,       0.45,       0,          0.05,       0,         0,      0,      0,      0],         # LAVA
    [0.65,      0,          0.3,        0.05,       0,         0,      0,      0,      0],         # HOLY
    [0.75,      0.1,        0.05,       0.05,       0.05,      0,      0,      0,      0],         # ROCK
    [0.6,       0,          0.005,      0.005,      0.3,       0,      0,      0,      0],         # VOID
    [1,         0,          0,          0,          0,         0,      0,      0,      0],         # EXIT
    [1,         0,          0,          0,          0,         0,      0,      0,      0],         # ENTRANCE
    [0.9,       0.03,       0.005,      0.04,       0.025,     0,      0,      0,      0],         # NONE
    [0,         0,          0,          0,          0,         0,      0,      0,      0]          # O_WALL
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

            if y == 0 and x == exit_index:      # preset entrances and exit points
                maptiles[0][exit_index] = TILE_ID["EXIT"]
            elif y == ylen-1 and x == enter_index:
                maptiles[y][enter_index] = TILE_ID["ENTER"]

            elif (y == 0 or y == ylen-1) or (x == 0 or x == xlen-1):        # border map with wall tiles
                maptiles[y][x] = TILE_ID["O_WALL"]

    return maptiles


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
    if (x < SIZE_X and y < SIZE_Y and x >= 0 and y >= 0):
       if grid[y][x] == TILE_ID["NONE"]:  # mostly generates horizontally, not a huge fan
        # generate tile
           newID = rand_select(prob_matrix, ID)
           grid[y][x] = newID
           grid = populate_grid(grid,x+1, y, newID)
           grid = populate_grid(grid,x, y+1, newID)
           grid = populate_grid(grid,x-1, y, newID)
           grid = populate_grid(grid,x, y-1, newID)

    return grid

def unblock_map(grid):      # ensures exits and entrances are not directly blocked by non-floor tiles
    for x in range(SIZE_X):
        if grid[0][x] == TILE_ID["EXIT"]:
            grid[1][x] = TILE_ID["FLOOR"]
        if grid[SIZE_Y-1][x] == TILE_ID["ENTER"]:
            grid[SIZE_Y-2][x] = TILE_ID["FLOOR"]
    
    return grid
    
def create_maplist():       # creates the list of maps which will be used for the game
    num_maps = r.randint(3, 5)
    maplist = [None] * num_maps
    print("Generating %s maps...\n" % num_maps)
    for i in range(num_maps):
        maptiles = init_grid(SIZE_X, SIZE_Y)        # to be rewritten, mostly output test            
        maplist[i] = unblock_map(populate_grid(maptiles, 1, 1, TILE_ID["EXIT"]))   # populates from exit
        
    return maplist, num_maps

############ MAP GEN FUNCS END ############

def main():
    global maptiles
    global SIZE_X
    global SIZE_Y
    global prob_matrix

    maplist, num_maps = create_maplist()
    for i in range(num_maps):
        print("MAP %s:\n" % (i+1))
        outgrid(maplist[i], SIZE_X, SIZE_Y)
        print()

main()


