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

SIZE_X = 25
SIZE_Y = 16
weight_matrix = [
   # FLOOR      LAVA        HOLY        ROCK        VOID      EXIT    ENTER   NONE    O_WALL        MATRIX OF TILE WEIGHTINGS, -1 = CANNOT GENERATE
    [500,       100,          0,        100,        100,      -1,     -1,     -1,     -1],         # FLOOR
    [0,         350,         -1,        150,        150,      -1,     -1,     -1,     -1],         # LAVA
    [100,        -1,        125,        175,        100,      -1,     -1,     -1,     -1],         # HOLY
    [180,       200,         25,        250,         50,      -1,     -1,     -1,     -1],         # ROCK
    [350,        50,         25,         25,        300,      -1,     -1,     -1,     -1],         # VOID
    [9999,       -1,         -1,         -1,         -1,      -1,     -1,     -1,     -1],         # EXIT
    [9999,       -1,         -1,         -1,         -1,      -1,     -1,     -1,     -1],         # ENTRANCE
    [450,       125,          5,        150,        120,      -1,     -1,     -1,     -1],         # NONE
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


def rand_select(weight_matrix, x, y, grid):     #select a tile type, given a tile next to it and a probability matrix
  sum_weights = [0] * len(TILE_ID)
  null_id = [0] * len(TILE_ID)
  total_weight = 0
  selected = False
  run_sum = 0
  z = -1
  selected_ID = 0

  new_x = x + 1
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

def populate_grid(grid, x, y, ID):      #populate given grid
    if (x < SIZE_X and y < SIZE_Y and x >= 0 and y >= 0):
       if grid[y][x] == TILE_ID["NONE"]:  # mostly generates horizontally, not a huge fan
        # generate tile
           newID = rand_select(weight_matrix, x, y, grid)
           grid[y][x] = newID
           grid = populate_grid(grid,x+1, y, newID)
           grid = populate_grid(grid,x, y+1, newID)


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
        maplist[i] = populate_grid(maptiles, 1, 1, TILE_ID["EXIT"])     # populates from exit
        
    return maplist, num_maps

############ MAP GEN FUNCS END ############

def main():
    global maptiles
    global SIZE_X
    global SIZE_Y
    global weight_matrix

    maplist, num_maps = create_maplist()
    for i in range(num_maps):
        print("MAP %s:\n" % (i+1))
        outgrid(maplist[i], SIZE_X, SIZE_Y)
        print()

main()

