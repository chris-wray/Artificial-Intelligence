class node:
    def __init__(self, value):
         self.value = value
         self.parent = None
         self.children = []
         self.depth = self.parent.depth+1

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

#prints tree in BFS order
def print_tree(root):
    queue = []
    visited = []

    while(len(queue) > 0):
        cur_node = queue.pop()
        visited.append(cur_node)

        for child in cur_node.children:
            queue.append(child)

def interpret_tree(string):
    op = -1 #op ==1 take max, op == -1 take min
    open_ind = 0
    close_ind = len(string)
    for i in range (0, len(string)):
        if(string[i] == '('): #first instance will set op to take max
            op = -op
            open_ind = i
            #print('Found ( at ' + str(i))

        if(string[i] == ')'): #work back from first leaf nodes
            #print('Found ) at ' + str(i))
            nums = []
            close_ind = i

            for j in range (open_ind, close_ind):
                if(string[j].isdigit()):
                    #print('found ' + string[j])
                    nums.append(int(string[j]))
            #print(nums)
            if(op == 1):
                return string.replace(string[open_ind:close_ind+1], str(max(nums))), nums.index(max(nums))
            else:
                #print('take min')
                return string.replace(string[open_ind:close_ind+1], str(min(nums))), nums.index(min(nums))
            #print('interpret_string' + string + '\t len(string): ' + str(len(string)))
            #interpret_tree(string)
            
                

def driver(string):
    count = 0
    nodes = []
    while(len(string) > 3):
        #print(str(count) + '\t' + string)
        string, index = interpret_tree(string)
        nodes.insert(0, index+1)
        #print('After:\t' + string)
        count +=1
    return string, nodes

tree = input('Enter a tree: ')

s, moves = driver(tree)

#print(s)
print(moves)
