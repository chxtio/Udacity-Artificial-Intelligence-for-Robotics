# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):
    print('{} x {} grid: '.format(len(grid), len(grid[0])))
    for i in range(len(grid)):
        print(grid[i])

    # 4 identical arrays the size of the grid concatenated
    value = [
        [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
        [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
        [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
        [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
    ]

    print('\nvalue: ')
    for i in range(len(value)):
        print(value[i])

    policy = [
        [[" " for col in range(len(grid[0]))] for row in range(len(grid))],
        [[" " for col in range(len(grid[0]))] for row in range(len(grid))],
        [[" " for col in range(len(grid[0]))] for row in range(len(grid))],
        [[" " for col in range(len(grid[0]))] for row in range(len(grid))],
    ]

    policy2D = [[" " for col in range(len(grid[0]))] for row in range(len(grid))]

    change = True
    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                for orientation in range(4):
                    # print(f"checking x {x}, yumn {y}")
                    if x == goal[0] and y == goal[1]:
                        if value[orientation][x][y] > 0:
                            value[orientation][x][y] = 0
                            policy[orientation][x][y] = "*"
                            print('\nchange value @ {},{},{} to 0'.format(orientation, x,y))
                            for i in range(len(value)):
                                print(value[i])
                            change = True

                    elif grid[x][y] == 0:
                        # Calculate the three ways to propogate the value
                        for i in range(3):
                            o2 = (orientation + action[i]) % 4
                            x2 = x + forward[o2][0]
                            y2 = y + forward[o2][1]

                            # Bounds checking- Still inside the grid and not at an obstacle
                            if x2 >= 0 and x2 < len(grid)and y2 >= 0 and y2 < len(grid[0]) \
                                    and grid[x2][y2] == 0:
                                new_value = value[o2][x2][y2] + cost[i]
                                if new_value < value[orientation][x][y]:
                                    value[orientation][x][y] = new_value
                                    policy[orientation][x][y] = action_name[i]
                                    change = True

    print('\n3D policy: ')
    for i in range(len(policy)):
        print(policy[i])

    # Convert from 3d policy to 2d policy by running the policy
    x, y, orientation = init[0], init[1], init[2]

    policy2D[x][y] = policy[orientation][x][y]
    while policy[orientation][x][y] != "*":
        if policy[orientation][x][y] == "#":
            o2 = orientation
        elif policy[orientation][x][y] == "R":
            o2 = (orientation - 1) % 4
        elif policy[orientation][x][y] == "L":
            o2 = (orientation + 1) % 4
        x = x + forward[o2][0]
        y = y + forward[o2][1]
        orientation = o2
        policy2D[x][y] = policy[orientation][x][y]

    return policy2D

policy = optimum_policy2D(grid,init,goal,cost)
print('\n2d policy: ')
for i in range(len(policy)):
    print(policy[i])

##5 x 6 grid:
##[1, 1, 1, 0, 0, 0]
##[1, 1, 1, 0, 1, 0]
##[0, 0, 0, 0, 0, 0]
##[1, 1, 1, 0, 1, 1]
##[1, 1, 1, 0, 1, 1]
##
##value:
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##
##change value @ 0,2,0 to 0
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##
##change value @ 1,2,0 to 0
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##
##change value @ 2,2,0 to 0
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##
##change value @ 3,2,0 to 0
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##[[999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [0, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999], [999, 999, 999, 999, 999, 999]]
##
##3D policy:
##[[' ', ' ', ' ', 'R', 'R', 'L'], [' ', ' ', ' ', '#', ' ', '#'], ['*', 'L', 'L', '#', 'L', 'L'], [' ', ' ', ' ', '#', ' ', ' '], [' ', ' ', ' ', '#', ' ', ' ']]
##[[' ', ' ', ' ', 'L', '#', '#'], [' ', ' ', ' ', 'R', ' ', 'L'], ['*', '#', '#', '#', '#', '#'], [' ', ' ', ' ', 'R', ' ', ' '], [' ', ' ', ' ', 'R', ' ', ' ']]
##[[' ', ' ', ' ', '#', 'R', '#'], [' ', ' ', ' ', '#', ' ', '#'], ['*', 'R', 'R', 'R', 'R', 'R'], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ']]
##[[' ', ' ', ' ', 'R', '#', 'R'], [' ', ' ', ' ', 'R', ' ', 'R'], ['*', '#', '#', 'L', '#', 'L'], [' ', ' ', ' ', 'L', ' ', ' '], [' ', ' ', ' ', 'L', ' ', ' ']]
##
##2d policy:
##[' ', ' ', ' ', 'R', '#', 'R']
##[' ', ' ', ' ', '#', ' ', '#']
##['*', '#', '#', '#', '#', 'R']
##[' ', ' ', ' ', '#', ' ', ' ']
##[' ', ' ', ' ', '#', ' ', ' ']
