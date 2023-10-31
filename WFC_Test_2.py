import random as r
import time
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

SIZE_X = 30
SIZE_Y = 15
weight_matrix = [
   # FLOOR      LAVA        HOLY        ROCK        VOID      EXIT    ENTER   NONE    O_WALL        MATRIX OF TILE WEIGHTINGS, -1 = CANNOT GENERATE
    [500,        35,          0,        100,         75,      -1,     -1,     -1,     -1],         # FLOOR              HORIZONTAL = ORIGINAL TILE
    [0,         350,         -1,         25,         25,      -1,     -1,     -1,     -1],         # LAVA
    [100,        -1,        125,        350,        100,      -1,     -1,     -1,     -1],         # HOLY
    [180,       150,         25,        250,         50,      -1,     -1,     -1,     -1],         # ROCK
    [350,        50,         25,         25,        300,      -1,     -1,     -1,     -1],         # VOID
    [9999,       -1,         -1,         -1,         -1,      -1,     -1,     -1,     -1],         # EXIT
    [9999,       -1,         -1,         -1,         -1,      -1,     -1,     -1,     -1],         # ENTRANCE
    [450,        65,          1,         60,         50,      -1,     -1,     -1,     -1],         # NONE
    [450,        50,         15,         50,        225,      -1,     -1,     -1,     -1]          # O_WALL
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


def entropy(grid):
    least_entropic_x = 0
    least_entropic_y = 0
    max_entropy = 5
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            entropy = 4
            if grid[y][x] == TILE_ID["NONE"]:
                if grid[y+1][x] != TILE_ID["NONE"]:
                    entropy -= 1
                if grid[y-1][x] != TILE_ID["NONE"]:
                    entropy -= 1
                if grid[y][x+1] != TILE_ID["NONE"]:
                    entropy -= 1
                if grid[y][x-1] != TILE_ID["NONE"]:
                    entropy -= 1
                if entropy < max_entropy:
                    max_entropy = entropy
                    least_entropic_x = x
                    least_entropic_y = y

    if max_entropy == 5:
        return -1, -1
    else:
        return least_entropic_x, least_entropic_y

def rand_select(weight_matrix, x, y, grid):     #select a tile type, given a tile next to it and a probability matrix
  sum_weights = [0] * len(TILE_ID)      # sum of weightings for each tile type
  null_id = [0] * len(TILE_ID)      # flags which tiles types are explicitly disallowed
  total_weight = 0      # the sum of all items in sum_weights (total weighting for that tile)
  selected = False      
  run_sum = 0       # running total of each weighting
  z = -1
  selected_ID = 0       # ID that the tile will collapse into

  new_x = x + 1     # sums weights from id of tile 
  new_y = y
  for i in range(len(TILE_ID)):
    if weight_matrix[grid[new_y][new_x]][i] != -1:
        sum_weights[i] += weight_matrix[grid[new_y][new_x]][i]
    else:
        null_id[i] = 1

  new_x = x - 1
  new_y = y
  for i in range(len(TILE_ID)):
    if weight_matrix[grid[new_y][new_x]][i] != -1:
        sum_weights[i] += weight_matrix[grid[new_y][new_x]][i]
    else:
        null_id[i] = 1
    
  new_x = x 
  new_y = y + 1
  for i in range(len(TILE_ID)):
    if weight_matrix[grid[new_y][new_x]][i] != -1:
        sum_weights[i] += weight_matrix[grid[new_y][new_x]][i]
    else:
        null_id[i] = 1

  new_x = x
  new_y = y - 1
  for i in range(len(TILE_ID)):
    if weight_matrix[grid[new_y][new_x]][i] != -1:
        sum_weights[i] += weight_matrix[grid[new_y][new_x]][i]
    else:
        null_id[i] = 1

  for i in range(len(sum_weights)):
    total_weight += sum_weights[i]
    
  randnum = r.randint(0, total_weight)
  while selected == False and z+1 < len(TILE_ID):
    z += 1
    run_sum += sum_weights[z]
    if randnum <= run_sum and null_id[z] != 1:
        selected = True
        selected_ID = z
      
  return selected_ID

def populate_grid(grid):      #populate given grid
    x, y = entropy(grid)
    while x != -1:
        newID = rand_select(weight_matrix, x, y, grid)
        grid[y][x] = newID
        x, y = entropy(grid)
        

    return grid
"""
def unblock_map(grid):      # ensures exits and entrances are not directly blocked by non-floor tiles
    for x in range(SIZE_X):
        if grid[0][x] == TILE_ID["EXIT"]:
            grid[1][x] = TILE_ID["FLOOR"]
        if grid[SIZE_Y-1][x] == TILE_ID["ENTER"]:
            grid[SIZE_Y-2][x] = TILE_ID["FLOOR"]
    
    return grid
"""  
def create_maplist():       # creates the list of maps which will be used for the game
    num_maps = r.randint(3, 5)
    maplist = [None] * num_maps
    print("Generating %s maps...\n" % num_maps)
    for i in range(num_maps):
        maptiles = init_grid(SIZE_X, SIZE_Y)                    
        maplist[i] = populate_grid(maptiles)     # populates from 1,1

    return maplist, num_maps

############ MAP GEN FUNCS END ############

def generate():
    global maptiles
    global SIZE_X
    global SIZE_Y
    global weight_matrix

    maplist, num_maps = create_maplist()

    return maplist, num_maps

if __name__ == "__main__":
    start = time.time()
    maplist, num_maps = generate()
    for i in range(num_maps):
        print("MAP %s:\n" % (i+1))
        outgrid(maplist[i], SIZE_X, SIZE_Y)
        print()
    end = time.time()
    print("%s seconds to generate %s maps" % (end-start, num_maps))

