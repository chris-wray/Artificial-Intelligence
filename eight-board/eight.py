import time
#import os
## 8puzzle solved with search algos

#used when generating children to not effect the parent
def cloning(state):
    state_copy = [x[:] for x in state]
    return state_copy


#used as key for sorting queue by h1
def sorth1(node):
    return node.h1

def sorth2(node):
    return node.h2

#used as key for sorting A* Algo
#for any node returns the sum of their parents heuristics
#and itself
def asorth1(node):
    val = node.h1
    while(node.parent):
        val = val + node.parent.h1
        node = node.parent
    return val

#same as above for h2
def asorth2(node):
    val = node.h2
    while(node.parent):
        val = val + node.parent.h2
        node = node.parent
    return val

def h1(node):
    win = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    score = 0
    for i in range (0, 3):
        for j in range(0, 3):
            #if space is not in right spot
            #add 1 to score
            if((win[i][j] != node.state[i][j]) and (node.state[i][j] != 0)):
                score +=1
    return score 

#Manhattan distance (summed)
def h2(node):
    win = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    score = 0
    #walk over every win position
    for i in range (0, 3):
        for j in range(0, 3):
            
            #walk over every node position
            for k in range (0, 3):
                for l in range(0, 3):

                    #if we have the coordinates for two matching spaces
                    if(node.state[k][l] == win[i][j]):
                        #Sum total spaces away space is from win position
                        difference = abs(i-k) + abs(j-l)
                        score = score + difference
    return score     

class board:

    def __init__(self, state, direction, parent, depth):
        self.state = state #2D array for board state
        self.children = [] #list of possible next moves
        self.parent = parent #previous board position
        self.direction = direction #direction moved from parent to generate self
        self.depth = depth #distance from root
        self.h1 = h1(self) #number of tiles out of place
        self.h2 = h2(self) #sum of manhattan distances of tiles

    def print_board(self):
        #print(self.direction)
        print('~~Score: ' + str(self.h1) + ',' + str(self.h2) +'~~~' + str(asorth1(self)) + '~~~~~~' + str(self.depth))
        for i in range (0, 3):
            for j in range(0, 3):
                print(str(self.state[i][j]) + '\t', end=" ")
            print('\n')  
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~') 

    def print_state(self):
        print("\n")
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for i in range (0, 3):
            for j in range(0, 3):
                print(str(self.state[i][j]) + '\t', end=" ")
            print('\n')  
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~') 
        print("\n")


    #Each state will have up to 4 children depending on the position of '0'
    def generate_children(self):
        #first find where the 'blank' space is
        a = None 
        b = None
        for i in range (0, 3):
            for j in range(0, 3):
                if(self.state[i][j] == 0): 
                    a, b = i, j

        #For each direction:
        #    make a copy of the original state
        #    switch the 'blank with another space as a 2D array
        #    make the new state a board
        #    add to the original states children

        #pushing up
        if(a > 0):
            temp = cloning(self.state)
            above = temp[a-1][b]
            temp[a-1][b] = 0
            temp[a][b] = above
            child = board(temp, "UP", self, self.depth+1)
            self.children.append(child)

        #pushing down
        if(a < 2):
            temp = cloning(self.state)
            below = temp[a+1][b]
            temp[a+1][b] = 0
            temp[a][b] = below
            child = board(temp, "DOWN", self, self.depth+1)
            self.children.append(child)

        #pushing right
        if(b < 2):
            temp = cloning(self.state)
            left = temp[a][b+1]
            temp[a][b+1] = 0
            temp[a][b] = left
            child = board(temp, "RIGHT", self, self.depth+1)
            self.children.append(child)

        #pushing left
        if(b > 0):
            temp = cloning(self.state)
            right = temp[a][b-1]
            temp[a][b-1] = 0
            temp[a][b] = right
            child = board(temp, "LEFT", self, self.depth+1)
            self.children.append(child)

    #Print each childs state
    def print_children(self):
        print('~~~~~~~~PRINTING CHILDREN~~~~~~~~')
        for child in self.children:
            print(child.direction)
            child.print_board()

    #determine whether selfs state is a win
    def check_win(self):
        win = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
        for i in range (0, 3):
            for j in range(0, 3):
                if(win[i][j] != self.state[i][j]):
                    return False
        #print('Win!')
        return True 


#BFS of the tree of states for a win
def BFS(root):
    max_queue_length = 0

    queue = []
    visited = []

    queue.append(root)

    start_time = time.time()

    while(len(queue) > 0):
        elapsed_time = time.time() - start_time
        if(elapsed_time > 600):
            return
        if(len(queue) > max_queue_length):
            max_queue_length = len(queue)
        cur_node = queue.pop(0)

        if(cur_node.check_win()):
            return [cur_node, max_queue_length, len(visited), elapsed_time]
        
        cur_node.generate_children()

        for child in cur_node.children:
            if(child.check_win()):
                return [child, max_queue_length, len(visited), elapsed_time]
            if(child.state not in visited):
                #append children to end of queue so all the nodes 
                # in the level above are expanded first
                visited.append(child.state)
                queue.append(child)


#always visit the first child node if it exists
#in this space there are a huge number of children so its not effective
def DFS(root):
    queue = []
    visited = []
    max_queue_length = 0
    queue.append(root)
    start_time = time.time()

    while(len(queue) > 0 ):
        elapsed_time = time.time()-start_time

        if(elapsed_time > 600):
            return
        
        if(len(queue) > max_queue_length ):
            max_queue_length = len(queue)

        cur_node = queue.pop(0)

        if(cur_node.check_win()):
            return [cur_node, max_queue_length, len(visited), elapsed_time]

        if(cur_node.state not in visited):
            visited.append(cur_node.state)
            cur_node.generate_children()
            for child in cur_node.children:
                #insert children at the front so they are expanded first
                queue.insert(0, child)

        
        print(str(len(visited)) + " nodes visited.. " + str(queue[0].depth) + " levels deep")


#Run DFS limit nodes deep
def DLS(root, limit):
    queue = []
    visited = []
    max_queue_length = 0
    start_time = time.time()
    queue.append(root)

    while(len(queue) > 0 ):
        cur_node = queue.pop(0)
        if(len(queue) > max_queue_length):
            max_queue_length = len(queue)
        elapsed_time = time.time()-start_time
        if(elapsed_time > 600):
            return
        if(cur_node.check_win()):
            return [cur_node, max_queue_length, len(visited), elapsed_time]


        if(cur_node.state not in visited):
            visited.append(cur_node.state)
            cur_node.generate_children()
            for child in cur_node.children:
                if(child.depth < limit):
                    queue.insert(0, child)

    return root,max_queue_length, len(visited), elapsed_time  

#Iterative deepening DFS
def IDS(root):
    depth = 1
    while True:
        #Run DLS for increasing depths
        #Makes DFS actually effective
        print("depth: " + str(depth))
        result, max_queue, visited, time = DLS(root, depth)
        if(result == root):
            depth = depth +1
        else:
            return result, max_queue, visited, time

#greedy always chooses the best scoring node in the queue
def greedy(root, h):
    max_queue_length = 0

    queue = []
    queue.append(root)
    visited = []

    start_time = time.time()
    #check each child for win state, also find the best child based on score
    while (len(queue) > 0):
        elapsed_time = time.time()-start_time

        if(len(queue) > max_queue_length):
            max_queue_length = len(queue)

        if(elapsed_time > 600):
            return
        
        best_node = queue.pop(0)
        best_node.generate_children()
        visited.append(best_node.state)

        for node in best_node.children:
            if(node.check_win()):
                return node, max_queue_length, len(visited), elapsed_time
            if(node.state not in visited):
                visited.append(node.state)
                queue.append(node)
        
        if(h == 1):
            queue.sort(key = sorth1)
        elif(h == 2):
            queue.sort(key = sorth2)

     
        #best scoring child saved as best_node
        #print("Greedy Score: " + str(sorth1(best_node)))

#a_star chooses the best scoring node in the queue
#score is the sum of a node score + its parents score all the way to the root
def a_star(root, h):
    max_queue_length = 0

    queue = []
    queue.append(root)
    visited = []
    
    start_time = time.time()
    #check each child for win state, also find the best child based on score
    while (len(queue) > 0):
        elapsed_time = time.time()-start_time

        if(len(queue) > max_queue_length):
            max_queue_length = len(queue)

        if(elapsed_time > 600):
            return

        best_node = queue.pop(0)
        best_node.generate_children()
        visited.append(best_node.state)


        for node in best_node.children:
            if(node.check_win()):
                return node, max_queue_length, len(visited), elapsed_time
            if(node.state not in visited):
                visited.append(node.state)
                queue.append(node)
        
        if(h == 1):
            queue.sort(key = asorth1)
        elif(h == 2):
            queue.sort(key = sorth2)

        #best scoring child will be best_node
        #print("A-Star Score: " + str(best_node.h1) + ', ' + str(asorth1(best_node)))
        
        

 #Easy: ’(1 3 4 8 6 2 7 0 5)
 #Medium: ’(2 8 1 0 4 3 7 6 5)
 #Hard: ’(5 6 7 4 0 8 3 2 1)

easy_start_state = [[1, 3, 4], [8, 6, 2], [7, 0, 5]]

med_start_state = [[2, 8, 1], [0, 4, 3], [7, 6, 5]]

hard_start_state = [[5, 6, 7], [4, 0, 8], [3, 2, 1]]

difficulty = int(input('Difficulty(int): (1=easy, 2=medium, 3=hard): '))

search = int(input('Search(int): \n1=BFS | 2=DFS | 3=IDS,\n4=Greedy with h1 | 5=Greedy with h2\n6=A* with h1 | 7=A* with h2\n:'))
root = None
if(difficulty == 1):
    root = board(easy_start_state, None, None, 0)
elif(difficulty == 2):
    root = board(med_start_state, None, None, 0)
elif(difficulty == 3):
    root = board(hard_start_state, None, None, 0)
else:
    print('Invalid difficulty')

if(search == 1):
    win_state, max_queue, visited, time = BFS(root)
elif(search == 2):
    win_state, max_queue, visited, time = DFS(root)
elif(search == 3):
    win_state, max_queue, visited, time = IDS(root)
elif(search == 4):
    win_state, max_queue, visited, time = greedy(root, 1)
elif(search == 5):
    win_state, max_queue, visited, time = greedy(root, 2)
elif(search == 6):
    win_state, max_queue, visited, time = a_star(root, 1)
elif(search == 7):
    win_state, max_queue, visited, time = a_star(root, 2)
else:
    print('Invalid search method')

#start algorithm

#start backtracking to print solution
moves = []
boards = []

#work up from win state recording parent and respective move direction
while(win_state.parent):
    moves.append(win_state.direction)
    boards.append(win_state.parent)
    win_state = win_state.parent

num_moves = len(moves)
#print from root to win state with directions
while(moves):
    board = boards.pop()
    #board.print_board()
    print(moves.pop(), end='\t')
#print('')

#print('Win in ' + str(num_moves) + " moves in " + str(time) + 's')
#print('Max Queue Length: ' + str(max_queue))
#print('Nodes visited: ' + str(visited))
