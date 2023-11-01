"""
TILE ID:
0 - None
1 - Grassland
2 - Coast
3 - Sea

RULES (adjacent only):
Grassland may only be adjoined by Sea and Grassland.
Sea may only be adjoined by Sea and Coast.
Coast can be adjoined by any other tile.
"""
import random as r

GRASS = 1
COAST = 2
SEA = 3
ID_ARR = ["N","G","C","S"]


def intgrid():
  global gridsize
  global grid
  global GRASS
  global COAST
  global SEA
  global ID_ARR
  
  gridsize = int(input("Gridsize? NxN"))
  grid = [[0]* gridsize for i in range(gridsize)]
  print(grid)


def outgrid(grid):
  for i in range(1, gridsize):
    str = ""
    for j in range(1 ,gridsize):
      str += "%s " % ID_ARR[grid[i][j]]

    print(str)
      

def adjcheck(id , x, y):
  xcheck = True
  ycheck = True
  if id == GRASS:
    for checkhoriz in range(-1,2):
      if (x+checkhoriz) < gridsize-1:
        if grid[y][x+checkhoriz] == SEA:
          xcheck = False
    for checkvert in range(-1,2):
      if (y+checkvert) < gridsize-1:
        if grid[y+checkvert][x] == SEA:
          ycheck = False
  elif id == SEA:
    for checkhoriz in range(-1,2):
      if (x+checkhoriz) < gridsize-1:
        if grid[y][x+checkhoriz] == GRASS:
          xcheck = False
    for checkvert in range(-1,2):
      if (y+checkvert) < gridsize-1:
        if grid[y+checkvert][x] == GRASS:
          ycheck = False

  if xcheck == True and ycheck == True:
    return True
  else:
    return False



def germinate():
  contarr = [False]*3
  for i in range(1, gridsize):
    for j in range(1, gridsize):
      allow = False
      while allow != True or ((contarr[0] == True and contarr[1] == True and contarr[2] == True) != True): 
        newid = r.randint(1,3)
        contarr[newid-1] = True
        print(contarr)
        print("Attempting %s at %s,%s" % (newid, j, i))
        allow = adjcheck(newid, j, i)
      print("####################################")
      if contarr[0] == True and contarr[1] == True and contarr[2] == True and allow == False:
        outgrid(grid)
        print("Contradiction Reached, tried to add %s at %s,%s" % (newid, j, i))
        quit()
      else:
        grid[i][j] = newid
        outgrid(grid)
        print("New addition %s at %s,%s" % (newid, j , i))
      contarr = [False]*3
      
def main():
  intgrid()
  germinate()

main()