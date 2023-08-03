import copy
import cProfile
from operator import attrgetter
import pstats
import re

# Creates the puzzle boards and Goal Board
myBoard0 = [[3, 1, 2],[7, "nil", 5],[4, 6, 8]]
myBoard1 = [[7, 2, 4],[5, "nil", 6],[8, 3, 1]]
myBoard2 = [[6, 7, 3],[1, 5, 2],[4, "nil", 8]]
myBoard3 = [["nil", 8, 6],[4, 1, 3],[7, 2, 5]]
myBoard4 = [[7, 3, 4],[2, 5, 1],[6, 8, "nil"]]
myBoard5 = [[1, 3, 8],[4, 7, 5],[6, "nil", 2]]
myBoard6 = [[8, 7, 6],[5, 4, 3],[2, 1, "nil"]]
goalBoard = [["nil", 1, 2],[3, 4, 5],[6, 7, 8]]
testGoal = [[1, 2, 3],[4, "nil", 5],[6, 7, 8]]


'''
Class Node which has a board (2D array), 
a parent (a Node), and a move (array)
'''
class Node:
    def __init__(self, b, p, m, c, d):
        self.board = b
        self.parent = p
        self.move = m
        self.cost = c
        self.depth = d


'''
Helper function - getNilRow()
Function called getNilRow which takes in a board as input
and returns the nil's row position as output
''' 
def getNilRow(board):
    nilRow = 0
    # Finds the row  for nil
    for row in range(3):
        for col in range(3):
            if(board[row][col] == "nil"):
                nilRow = row
    return nilRow

'''
Helper function - getNilCol()
Function called getNilCol which takes in a board as input
and returns the nil's column position as output
''' 
def getNilCol(board):
    nilCol = 0
    # Finds the column for nil
    for row in range(3):
        for col in range(3):
            if(board[row][col] == "nil"):
                nilCol = col
    return nilCol

'''
Helper function - printBoard()
Function called printBoard which takes in a board
and prints the board in a readable format where 
each row is on a new line
'''
def printBoard(board):
    print(board[0])
    print(board[1])
    print(board[2])
    print("")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 1

'''
Part 1
Function called possible_actions that takes in a board as input
and outputs a list of all actions possible on the given board
'''
def possible_actions(board):

    # Initializes the array to hold all possible actions
    actionsArray = []

    # Initiallizes variables for the nil's row and column position
    nilRow = getNilRow(board)
    nilCol = getNilCol(board)
    
    # Handles possible actions for Up and Down
    if(nilRow == 0):
        action = ["Up", 1, nilCol]
        actionsArray.append(action)
    if(nilRow == 1):
        actionA = ["Up", 2, nilCol]
        actionB = ["Down", 0, nilCol]
        actionsArray.append(actionA)
        actionsArray.append(actionB)
    if(nilRow == 2):
        action = ["Down", 1, nilCol]
        actionsArray.append(action)
    
    # Handles possible actions for Left and Right
    if(nilCol == 0):
        action = ["Left", nilRow, 1]
        actionsArray.append(action)
    if(nilCol == 1):
        actionA = ["Left", nilRow, 2]
        actionB = ["Right", nilRow, 0]
        actionsArray.append(actionA)
        actionsArray.append(actionB)
    if(nilCol == 2):
        action = ["Right", nilRow, 1]
        actionsArray.append(action)

    return actionsArray



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 2

'''
Part 2
Function called result that takes in an action and a board as input
and outputs a new board that will result after carrying out the input move
'''
def result(action, board):
    
    # Initializes the newBoard by making a copy of the inputted board
    newBoard = copy.deepcopy(board)

    # Finds the row and column of nil of the inputted board
    oldNilRow = getNilRow(board)
    oldNilCol = getNilCol(board)

    # Sets the nil to the new number,
    # and sets that number's original position to nil
    myNum = newBoard[action[1]][action[2]]
    newBoard[oldNilRow][oldNilCol] = myNum
    newBoard[action[1]][action[2]] = "nil"
            
    return newBoard



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 3

'''
Part 3
Function called expand that takes in a board as input,
and outputs a list of all states that can be 
reaches in one action from the given state
'''
def expand(board):
    
    # Initializes allStates which is an array that will hold
    # all the boards after executing each possible action
    allStates = []

    # Calls the possible_actions function to get all the possible actions given a board, 
    # and calls the result function and adds each new board to the allStates array 
    myPossibleActions = possible_actions(board)
    for action in myPossibleActions:
        allStates.append(result(action, board))

    return allStates



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 4
'''
Part 4
Function called search which takes in an 
initial board and goal board as input and
outputs a list of acitons that form an optimal path 
from the initial board to the goal board
'''
def search(initialBoard, goalBoard):
    
    # Inititialize the depth to 1
    maxDepth = 1

    # Initializes an array that will hold the action sequence
    actions = []

    # While loop to keep searching for the goal board
    while True:
        
        # Calls the iterativeDeepening function and 
        # returns the goal board as the result and 
        # the array of actions to reach the goal board
        result, actions = iterativeDeepening(initialBoard, goalBoard, 0, maxDepth, actions)

        # If the result is not None, then the goal board was found
        if result is not None:

            # The array of actions must be reversed, since recursion (LIFO) was used
            actions.reverse()

            # Returns the sequence of actions that form the optimal path
            # from the intial board to the goal board
            return actions

        # maxDepth is incremeneted by 1 
        # The goal board was not found, but the 
        # goal board may be found deeper in the tree
        maxDepth = maxDepth + 1

    

    # The Bottom of the tree was reached, and the goal board was not found,
    # And there were no more boards with children to explore at a higher depth
    return None

'''
Helper function - iterativeDeepening()
Function called iterativeDeepening which takes in 
a board, goalBoard, currentDepth, maxDepth, and actions
and outputs a board and a list of actions
'''
def iterativeDeepening(board, goalBoard, currentDepth, maxDepth, actions):

    # Initializes an array called children, which calls the expand function 
    # and holds all the boards that are children of the initial board
    children = expand(board)

    # Initializes an array called moves, which hold the possible actions given a board
    moves = possible_actions(board)

    # If the board is equal to the goalBoard, then the goalBoard was found
    # Returns the board and the actions to reach the goal board
    if board == goalBoard:
        return board, actions
    
    # When the current depth is equal to the max depth then 
    # the goal board was not found yet, so returns None
    if currentDepth == maxDepth:
        return None, actions

    # Searches through the children
    for i in range(len(children)):

        # Recursively calls the function iterativeDeepening() and 
        # passes in the current child board
        result, actions = iterativeDeepening(children[i], goalBoard, currentDepth+1, maxDepth, actions)

        # Adds the child board's move to actions
        actions.append(moves[i])

        # If the result is not None then the goal board was found
        # And returns the result which is the goal board
        # and also returns the sequence of actions
        if result is not None:
            return result, actions
        
        # If this code is reached, then the goal board was not found, 
        # and the move that was added is not part of the action sequence
        # so the last action is removed
        actions.pop()
    

    # All children were seached and the goal board was not found
    return None, []







#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 5

'''
Helper function - findAstarActions()
Function called findAstarActions which takes in a node
and returns the list of actions from that node to the root node
'''
def findActions(endNode):
    
    currentNode = endNode
    actions = []

    # Loop that continues until it reaches the root node
    # Adds the currentNode's move to the actions array
    # Then sets the currentNode to its parent
    while currentNode.parent is not None:
        actions.append(currentNode.move)
        currentNode = currentNode.parent

    # Actions are reversed since they are initially listed from end to start
    actions.reverse()

    return actions


'''
Helper function - hash
Hash takes in a node and returns a unqiue hash code as a string
'''
def hash(myNode):

    # Loops through the node's board and creates a 
    # unique string from each number in the board
    hashCode = ""
    for row in range(3):
        for col in range(3):
            myCharacter = str(myNode.board[row][col])
            hashCode = hashCode + myCharacter
    return hashCode
    

'''
Part 5
Function called breadthFirstSearch which takes 
in an initial board and goal board as input and
outputs an optimal sequence of actions that form 
an optimal path from the initial board to the goal board
'''
def breadthFirstSearch(initialBoard, goalBoard):

    # Initialize the start node
    startNode = Node(initialBoard, None, None, 0, 0)

    # Initializes queue which holds the nodes that have not been visited yet 
    # Ands adds the initial node to the queue
    queue = []
    queue.append(startNode)

    # The currentNode is initialized to the start node
    currentNode = startNode

    # Initializes visited which is a dictionary that holds
    # the hash codes for each board that has been checked
    visited = {}

    # If the starting Board is already equal to the 
    # goal board then it returns
    if(currentNode.board == goalBoard):
        return []
    

    # Loop runs while queue is not empty
    while queue:
        
        # Removes the first board in the queue 
        # and stores that board in currentBoard
        currentNode = queue.pop(0)

        # Checks if the currentBoard is the same as the goalBoard
        # The goal Board was found!
        if(currentNode.board == goalBoard):
            # Calls the findActions function and returns the list of actions
            return findActions(currentNode)
        elif hash(currentNode) in visited:
            # If the hash of the current node is already 
            # in the visited dictionary, then continue
            continue
        else:
            # Calls the hash function, given the currentNode
            # Adds the hash as the key in the visited dictionary
            visited[hash(currentNode)] = 1

        # Initializes an array called children, which calls the expand function 
        # and holds all the boards that are children of the initial board
        children = expand(currentNode.board)

        # Initializes an array called moves, which hold the possible actions given a board
        moves = possible_actions(currentNode.board)

        # Loops through all the children boards
        for i in range(len(children)):
            # Creates a new node for that child board and 
            # adds the new node to the queue 
            queue.append(Node(children[i], currentNode, moves[i], 0, 0))
    
    return None



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 6

'''
Heuristic function called heuristicZero
which returns a heuristic of 0
'''
def heuristicZero(board, goalBoard):
    return 0

'''
Heuristic function called numMisplacedTiles
which takes in a board and goal bpard as input 
and returns the number of tiles that are 
misplaced on the board as output
'''
def numMisplacedTiles(board, goalBoard):
    
    misplacedTiles = 0

    # Loops through the board and goalBoard and checks if 
    # each corresponding position have the same value
    for row in range(3):
        for col in range(3):
            if(board[row][col] != goalBoard[row][col]):
                # Adds 1 to the misplaced tiles if the value in 
                # the board doesn't equal the value int he goal board 
                # at the same position 
                misplacedTiles = misplacedTiles + 1
    
    return misplacedTiles


'''
Heuristic function called manhattenDistance which 
takes in a board and goal board as inpit
and returns the Manhatten Distance
'''
def manhattenDistance(board, goalBoard):
    manDist = 0

    # Outer loop that goes through the board
    for row in range(3):
        for col in range(3):
            # Inner loop that goes through the goalBoard
            for r in range(3):
                for c in range(3):
                    if board[row][col] == goalBoard[r][c]:
                        # Finds the distance of a number to its goal position
                        # and adds the distance to the manhattan distance
                        manDist = manDist + abs(row - r) + abs(col - c)
    return manDist



'''
Part 6
Function called Astar which implments an A* search
It takes in an initial goal, a goal board, and a
heuristic function, and it returns a sequence of actions
to go from the initial board to the goal board as output
'''
def Astar(initialBoard, goalBoard, heuristicFunc):

    # Initialize the start node
    startNode = Node(initialBoard, None, None, 0, 0)

    # Creates an array called openNodes which will hold the unvisited nodes
    # And adds the start node into openNodes
    openNodes = []
    openNodes.append(startNode)

    # The currentNode is initialized to the start node
    currentNode = startNode

    # Initializes visited which is a dictionary that holds
    # the hash codes for each board that has been checked
    visited = {}

    # If the starting Board is already equal to the 
    # goal board then it returns
    if(currentNode.board == goalBoard):
        return []

    # The lowestCost keeps track of the value of the 
    # lowest cost given a board, depending on which heuristic is used
    lowestCost = heuristicFunc(startNode.board, goalBoard)

    # Loop runs while there are nodes in openNodes
    while openNodes:

        # Sets the current node to the first node in the openNodes list
        # which should be the node with the lowest cost
        currentNode = openNodes.pop(0)

        # Calls the hash() function to find the currentNode's hash
        currentHash = hash(currentNode)
        
        # Checks if the currentBoard is the same as the goalBoard
        # The goal Board was found!
        if(currentNode.board == goalBoard):
            # Calls the findActions function and returns the list of actions
            return findActions(currentNode)
        elif currentHash in visited:
            # If the hash of the current node is already 
            # in the visited dictionary, then continue
            continue
        else:
            # Adds the hash as the key in the visited dictionary
            visited[currentHash] = 1
        
        # Initializes an array called children, which calls the expand function 
        # and holds all the boards that are children of the initial board
        children = expand(currentNode.board)

        # Initializes an array called moves, which hold the possible actions given a board
        moves = possible_actions(currentNode.board)

        # Sets the depth for the children nodes
        nextDepth = currentNode.depth + 1

        # Loops through all the children boards
        for i in range(len(children)):
            # Creates a new node for that child board and 
            # adds the new node to the queue 
            openNodes.append(Node(children[i], currentNode, moves[i], heuristicFunc(currentNode.board, goalBoard) + nextDepth, nextDepth))
        
        # Sort the openNodes list by cost, with the node with the lowest cost first
        openNodes = sorted(openNodes, key=attrgetter("cost"))

    return None



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 7




        



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main

def main():
    
    # Note - Uncomment each of the print statements to run each test

    # Part 4 Test - iterative deepening search
    print(search(myBoard0, goalBoard))

    # Part 5 Test - breadth first search
    #print(breadthFirstSearch(myBoard0, goalBoard))
    #print(breadthFirstSearch(myBoard1, goalBoard))

    # Part 6.1 Test - A* with heuristicZero
    #print(Astar(myBoard0, goalBoard, heuristicZero))

    # Part 6.2 Test - A* with Number of misplaced tiles heuristic,
    # and manhatten distance heuristic
    #print(Astar(myBoard0, goalBoard, numMisplacedTiles))
    #print(Astar(myBoard0, goalBoard, manhattenDistance))
    #print(Astar(myBoard1, goalBoard, numMisplacedTiles))
    #print(Astar(myBoard1, goalBoard, manhattenDistance))



    # Part 7.1 Test

    # print(search(myBoard0, goalBoard))
    # 622897 function calls (556254 primitive calls) in 0.274 seconds

    # print(breadthFirstSearch(myBoard0, goalBoard))
    # 47121 function calls (42441 primitive calls) in 0.023 seconds
    
    # print(Astar(myBoard0, goalBoard, manhattenDistance))
    # 10636 function calls (9871 primitive calls) in 0.006 seconds



    # Part 7.2 Test
    
    # print(Astar(myBoard2, goalBoard, numMisplacedTiles))
    # 3849447 function calls (3475422 primitive calls) in 10.082 seconds
    
    # print(Astar(myBoard2, goalBoard, manhattenDistance))
    # 653509 function calls (606454 primitive calls) in 0.443 seconds




    # Part 7.3 Test
    
    # print(breadthFirstSearch(myBoard2, goalBoard))
    # 25167564 function calls (22673304 primitive calls) in 24.036 seconds

    # print(breadthFirstSearch(myBoard3, goalBoard))
    # 50707959 function calls (45704769 primitive calls) in 66.396 seconds
    
    # print(breadthFirstSearch(myBoard4, goalBoard))
    # 34076857 function calls (30705997 primitive calls) in 36.815 seconds
    
    # print(breadthFirstSearch(myBoard5, goalBoard))
    # 41372066 function calls (37281431 primitive calls) in 49.213 seconds
    
    # print(breadthFirstSearch(myBoard6, goalBoard))
    # 72855395 function calls (65714195 primitive calls) in 106.929 seconds


    #print(Astar(myBoard2, goalBoard, manhattenDistance))
    # 653509 function calls (606454 primitive calls) in 0.442 seconds
    
    # print(Astar(myBoard3, goalBoard, manhattenDistance))
    # 1512653 function calls (1403603 primitive calls) in 1.374 seconds

    # print(Astar(myBoard4, goalBoard, manhattenDistance))
    #  885467 function calls (821687 primitive calls) in 0.652 seconds

    # print(Astar(myBoard5, goalBoard, manhattenDistance))
    # 3156925 function calls (2929540 primitive calls) in 4.309 seconds

    # print(Astar(myBoard6, goalBoard, manhattenDistance))
    # 1371276 function calls (1272381 primitive calls) in 1.198 seconds



if __name__ == '__main__':
    cProfile.run("main()")
   
    




    
