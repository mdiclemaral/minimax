"""
Maral Dicle Maral

May 2021

In this project, an 8-tile game with 3 competing agents is created.
3 different algorithms, namely minimax, minimax_rand and alpha-beta pruning were implemented.
In minimax and alpha-beta pruning, all three agents were rational while in minimax_rand
Agent 2 and 3 are doing random moves. (the first move that was created)
Agent 1 can only move the odd tiles, agent 2 can only move the even tiles while agent 3 can move all tiles.

"""
import sys
u = 0

class Node:  #Stores tile boards
    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.shift = None
        self.cost = 0
        self.num_costs = []
        self.num_dict = {}
        self.h = 0
        self.f = 0
        self.children = []
        self.value = None

    def child_born(self, agent):  # Creates a new board with new tile configuration
        if agent == "agent1":
            num_costs, num_dict = self.find_number1()
        elif agent == "agent2":
            num_costs, num_dict = self.find_number2()
        else:
            num_costs, num_dict = self.find_number3()
        for cost in num_costs:
            new_positions = []
            x = num_dict[cost][0]
            y = num_dict[cost][1]
            new_positions.extend([[x-1, y, " left"], [x+1, y, " right"], [x, y-1, " up"], [x, y+1, " down"]])  #left right up down
            for j in new_positions:
                child = self.shift_position(x, y, j[0], j[1])
                if child is not None:
                    childN = Node(child, self)
                    childN.shift = "move " + str(cost) + j[2]
                    childN.cost = cost + childN.parent.cost
                    self.children.append(childN)

    def shift_position(self, x1, y1, x2, y2):  # Shifts the positions to the given directions

        child = self.copy(self.data)
        if (x2>= 0 and y2>= 0 and x2 < len(self.data) and y2 < len(self.data)):

            if self.data[y2][x2] == ".":
                temp_pos = child[y2][x2]
                child[y2][x2] = child[y1][x1]
                child[y1][x1] = temp_pos
                return child
            else:
                return None
        else:
            return None

    def copy(self, node):  # Creates a copy of the current board
        temp = []
        for i in range(0, len(node)):
            t = node[i].copy()
            temp.append(t)
        return temp

    def find_number1(self):  # Finds the positions of the tiles for agent 1 (only odd tiles)
        num_costs = []
        number_found = {}
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                temp_tile = self.data[i][j]
                if not (temp_tile == "." or temp_tile == "x"):
                    num_tile = int(temp_tile)
                    if (num_tile % 2) == 1:
                        num_costs.append(num_tile)
                        number_found[num_tile] = [j, i]
        return num_costs, number_found

    def find_number2(self):  # Finds the positions of the tiles for agent 2 (only even tiles)
        num_costs = []
        number_found = {}
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                temp_tile = self.data[i][j]
                if not (temp_tile == "." or temp_tile == "x"):
                    num_tile = int(temp_tile)
                    if (num_tile % 2) == 0:
                        num_costs.append(num_tile)
                        number_found[num_tile] = [j, i]
        return num_costs, number_found

    def find_number3(self):  # Finds the positions of the tiles for agent 3 (all kinds of tiles)
        num_costs = []
        number_found = {}
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                temp_tile = self.data[i][j]
                if not (temp_tile == "." or temp_tile == "x"):
                    current_tile = int(temp_tile)
                    num_costs.append(current_tile)
                    number_found[current_tile] = [j, i]
        return num_costs, number_found


class Puzzle:  # Puzzle class to store the whole puzzle
    def __init__(self, innput, outtput):
        self.innput = innput
        self.outtput = outtput
        #self.search_type = search_type
        self.start = None
        self.goal = None
        self.goal_tiles = None
        self.goal_dict = None
        self.actions = []
        self.createPuzzle()

    def createPuzzle(self):  # Creates the initial and goal nodes and initiates the puzzle
        final_input = []
        final_goal = []

        for i in range(0,len(self.innput)):

            temp_input = self.innput[i].split()
            final_input.append(temp_input)

            temp_goal = self.outtput[i].split()
            final_goal.append(temp_goal)

        self.start = Node(final_input, None)
        self.goal = Node(final_goal, None)
        self.goal_tiles, self.goal_dict = self.goal.find_number3()

    def minimax_decision(self,state, n, a_type):  # For all the recursive minimax algorithms to start
        if a_type == "minimax":
            val, actions = self.agent1(state, 0, n)
        elif a_type == "minimax_rand":
            val, actions = self.agent1_ex(state, 0, n)
        elif a_type == "alpha_beta_pruning":
            a = -sys.maxsize
            b = sys.maxsize
            val, actions = self.agent1_ab(state, 0, n, a, b)
        else:
            print("Please rewrite the search type")
            val, actions = None, None
        return val, actions

######   MINIMAX   #######

    def agent1(self, state, depth, n):
        temp = None
        tempList = None
        if depth == n:
            return self.utility(state)
        depth += 1
        self.actions.append(state)
        v = -sys.maxsize
        state.child_born("agent1")
        for c in state.children:
            new, actions = self.agent2(c, depth, n)
            if new > v:
                temp = c
                v = new
                tempList = actions
        tempList.append(temp)
        return v, tempList

    def agent2(self, state, depth, n):
        temp= None
        tempList = None
        v = sys.maxsize
        state.child_born("agent2")
        self.actions.append(state)
        for c in state.children:
            new, actions = self.agent3(c, depth, n)
            if new < v:
                temp = c
                v = new
                tempList = actions
        tempList.append(temp)
        return v, tempList

    def agent3(self, state, depth, n):
        temp = None
        tempList = None
        v = -sys.maxsize
        state.child_born("agent3")
        self.actions.append(state)
        for c in state.children:
            new, actions = self.agent1(c, depth, n)
            if new > v:
                temp = c
                v = new
                tempList = actions
        tempList.append(temp)
        return v, tempList

    ######   ALPHA-BETA PRUNING  #######
    def agent1_ab(self, state, depth, n, a, b):
        temp = None
        tempList = None
        if depth == n:
            return self.utility(state)
        v = -sys.maxsize
        depth += 1
        state.child_born("agent1")
        for c in state.children:
            new, actions = self.agent2_ab(c, depth, n, a, b)
            #v = max(new, v)
            if new > v:
                v = new
                temp = c
                tempList = actions
            if v >= b:
                return v, tempList
            a = max(a, v)
        tempList.append(temp)
        return v, tempList

    def agent2_ab(self, state, depth, n, a, b):
        temp = None
        tempList = None
        v = sys.maxsize
        state.child_born("agent2")
        for c in state.children:
            new, actions= self.agent3_ab(c, depth, n, a, b)
            #v = min(new, v)
            if new < v:
                v = new
                temp =c
                tempList = actions
            if v <= a:
                return v, tempList
            b = min(b, v)
        tempList.append(temp)
        return v, tempList

    def agent3_ab(self, state, depth, n, a, b):
        temp = None
        tempList = None
        v = -sys.maxsize
        state.child_born("agent3")
        for c in state.children:
            new, actions= self.agent1_ab(c, depth, n, a, b)
            #v = max(new, v)
            if new > v:
                v = new
                temp = c
                tempList = actions
            if v >= b:
                return v, tempList
            a = max(a, v)
        tempList.append(temp)
        return v, tempList

    ######   MINIMAX RANDOM  #######

    def agent1_ex(self, state, depth, n):  # Rational agent
        temp = None
        tempList = None
        if depth == n:
            return self.utility(state)
        v = -sys.maxsize
        depth += 1
        state.child_born("agent1")
        for c in state.children:
            new, actions = self.agent2_ex(c, depth, n)
            #v = max(new, v)
            if new > v:
                v = new
                temp = c
                tempList = actions
        tempList.append(temp)
        return v, tempList

    def agent2_ex(self, state, depth, n):  # Random agent
        tempList = None
        v = 0
        count = 0
        state.child_born("agent2")
        for c in state.children:
            temp_val, actions = self.agent3_ex(c, depth, n)
            if count == 0:
                tempList = actions
                tempList.append(c)
            v += temp_val
            count += 1
        return v/count, tempList

    def agent3_ex(self, state, depth, n):  # Random agent
        tempList = None
        v = 0
        count = 0
        state.child_born("agent3")
        for c in state.children:
            temp_val, actions = self.agent1_ex(c, depth, n)
            if count == 0:
                tempList = actions
                tempList.append(c)
            v += temp_val
            count += 1
        return v/count, tempList

    def utility(self, current):  # Utility calculating function
        global u
        u += 1
        util = 0
        for i in self.goal_tiles:
            [x, y] = self.goal_dict[i]
            current_tile = current.data[y][x]
            if current_tile == str(i):
                num_tile = int(current_tile)
                if (num_tile % 2) == 1:
                    util += num_tile
                else:
                    util -= num_tile
        return util, []


# For file handling and creating the game

game_type = sys.argv[1]
init = sys.argv[2]
goal = sys.argv[3]
depth = int(sys.argv[4])
soln = sys.argv[5]

with open(init) as file_initial:
    input_initial = file_initial.readlines()

with open(goal) as file_goal:
    input_final = file_goal.readlines()

puzz = Puzzle(input_initial, input_final)
value, actions = puzz.minimax_decision(puzz.start, depth, game_type)

f = open(soln, 'w')

for i in range(0, len(actions)):
    if i % 3 == 0:
        f.write("AGENT1 ")
    elif i % 3 == 1:
        f.write("AGENT2 ")
    else:
        f.write("AGENT3 ")
    act = actions.pop()
    f.write(act.shift +  "\n")

f.write("Value: "+("{:.2f}".format(value))+"\n")
f.write("Util calls: " + str(u) + "\n")

