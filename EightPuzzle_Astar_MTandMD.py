#!usr/bin/env python
"""
@Author: James Rolfe
@Date: 11 November 2015
@File: EightPuzzle_Astar_MTandMD.py
@Purpose: This python program will perform A* search using both the Manhattan Distance and 
			Misplaced Tiles Heuristics added together to find a solution path for the 8 puzzle 
			problem. Everything is hardcoded in so all you need to do is run it 'python EightPuzzle_Astar_MTandMD.py' 
			--created using python3.4.3
"""
import time
import math
import heapq

class Node:
	
	def __init__(self, puzzle, last=None):
		self.puzzle = puzzle
		self.last = last
		self.gCost = None # save path cost
		self.hCost = self.getHCost() # save heuristic cost
		self.fCost = None

	@property
	def seq(self): # to keep track of the sequence used to get to the goal
		node, seq = self, []
		while node:
			seq.append(node)
			node = node.last
		yield from reversed(seq)

	@property
	def state(self):
	    return str(self.puzzle.board) # hashable so it can be compared in sets

	@property
	def isSolved(self):
		return self.puzzle.isSolved # wrapper
    
	@property
	def getMoves(self):
	    return self.puzzle.getMoves # wrapper

	def getMTcost(self):
		"""
		A* Heuristic where the next node to be expanded is chosen based upon how 
		many misplaced tiles (MT) are in the state of the next node 
		"""
		totalMTcost = 0
		b = self.puzzle.board[:]
		# simply +1 if the tile isn't in the goal position
		# the zero tile doesn't count
		if b[1] != 1:
			totalMTcost += 1
		if b[2] != 2:
			totalMTcost += 1
		if b[3] != 3:
			totalMTcost += 1
		if b[4] != 4:
			totalMTcost += 1
		if b[5] != 5:
			totalMTcost += 1
		if b[6] != 6:
			totalMTcost += 1
		if b[7] != 7:
			totalMTcost += 1
		if b[8] != 8:
			totalMTcost += 1

		return totalMTcost

	# finds the distance between each tile's current position and goal position (non-diagonal movements)
	def getMD(self):
		manhattanDistance = 0
		copyBoard = self.puzzle.board[:]
		copyPuzzle = Puzzle(copyBoard)
		puzz2D = copyPuzzle.to2D # make the puzzle 2D, couldn't think of a quick 1D MD calculator
		for row in range(3): # only works for 3x3 puzzle
			for col in range(3):
				tile = puzz2D[row][col]
				if tile != 0:
					expectedRow = ((tile - 1) / 3) # find individual tile's goal position
					expectedCol = ((tile - 1) % 3) # ^
					rowDiff = row - expectedRow
					colDiff = col - expectedCol
					manhattanDistance += (math.fabs(rowDiff) + math.fabs(colDiff))
		return manhattanDistance

	def getHCost(self):
		totalHeuristicCost = self.getMTcost() + self.getMD() # Manhattan Distance plus Misplace Tiles
		return totalHeuristicCost

	def getGCost(self):
	    return self.gCost

	def getFCost(self):
		if self.gCost != None: # fCost won't exist for the starting node
			return self.getGCost() + self.getHCost()
		else:
			return self.getHCost()

	def setGCost(self, num):
		self.gCost = num
	

class Puzzle:

	def __init__(self, startBoard):
		self.board = startBoard

	@property
	def getMoves(self):
		
		possibleNewBoards = []

		zeroPos = self.board.index(0) # find the zero tile to determine possible moves
		# all possible moves hardcoded
		if zeroPos == 0:
			possibleNewBoards.append(self.move(0,1))
			possibleNewBoards.append(self.move(0,3))
		elif zeroPos == 1:
			possibleNewBoards.append(self.move(1,0))
			possibleNewBoards.append(self.move(1,2))
			possibleNewBoards.append(self.move(1,4))
		elif zeroPos == 2:
			possibleNewBoards.append(self.move(2,1))
			possibleNewBoards.append(self.move(2,5))
		elif zeroPos == 3:
			possibleNewBoards.append(self.move(3,0))
			possibleNewBoards.append(self.move(3,4))
			possibleNewBoards.append(self.move(3,6))
		elif zeroPos == 4:
			possibleNewBoards.append(self.move(4,1))
			possibleNewBoards.append(self.move(4,3))
			possibleNewBoards.append(self.move(4,5))
			possibleNewBoards.append(self.move(4,7))
		elif zeroPos == 5:
			possibleNewBoards.append(self.move(5,2))
			possibleNewBoards.append(self.move(5,4))
			possibleNewBoards.append(self.move(5,8))
		elif zeroPos == 6:
			possibleNewBoards.append(self.move(6,3))
			possibleNewBoards.append(self.move(6,7))
		elif zeroPos == 7:
			possibleNewBoards.append(self.move(7,4))
			possibleNewBoards.append(self.move(7,6))
			possibleNewBoards.append(self.move(7,8))
		else:
			possibleNewBoards.append(self.move(8,5))
			possibleNewBoards.append(self.move(8,7))

		return possibleNewBoards # returns Puzzle objects (maximum of 4 at a time)

	def move(self, current, to):

		changeBoard = self.board[:] # create a copy
		changeBoard[to], changeBoard[current] = changeBoard[current], changeBoard[to] # switch the tiles at the passed positions
		return Puzzle(changeBoard) # return a new Puzzle object

	def printPuzzle(self): # prints board in 8 puzzle style
		
		copyBoard = self.board[:]
		for i in range(9):
			if i == 2 or i == 5:
				print(str(copyBoard[i]))
			else:
				print(str(copyBoard[i])+" ", end="")
		print('\n')

	@property
	def isSolved(self):
		return self.board == [0,1,2,3,4,5,6,7,8] # goal board

	@property
	def to2D(self): # returns a 2D array representation of the puzzle.board
		copyBoard = self.board[:]
		my2Darray = [[0,0,0],[0,0,0],[0,0,0]] # fill with zeros
		for i in range(len(copyBoard)):
			index = copyBoard.index(i)
			if index <= 2:
				row = 0
				col = index
			elif index > 2 and index <= 5:
				row = 1
				col = index - 3
			else:
				row = 2
				col = index - 6
			my2Darray[row][col] = self.board[i]
		return my2Darray
	

class Solver:

	def __init__(self, Puzzle):
		self.puzzle = Puzzle

	def FindLowestMTcost(NodeList):
		print(len(NodeList))
		lowestMTcostNode = NodeList[0]
		lowestMTcost = lowestMTcostNode.getMTcost()
		for i in range(len(NodeList)):
			if NodeList[i].getMTcost() < lowestMTcost:
				lowestMTcostNode = NodeList[i]
		return lowestMTcostNode # returns Node object

	def AStarMT(self):
		my_queue = []
		visited = set() # don't get stuck in loop
		heapq.heappush(my_queue,(0,0,Node(self.puzzle))) # priority queue
		tieBreaker = 1
		while my_queue:
			bestChild = heapq.heappop(my_queue)[2] # [2] is to get the Node()
			visited.add(bestChild.state)
			if bestChild.isSolved:
				return bestChild.seq
			childList = []
			for board in bestChild.getMoves:
				newChild = Node(board, bestChild)
				if newChild.state not in visited:
					childList.append(newChild)
			for node in childList:
				if bestChild.getGCost() != None:
					node.setGCost(bestChild.getGCost() + 1) # calculate path cost for each node
				else:
					node.setGCost(1) # for children of the starting node
				heapq.heappush(my_queue, (node.getFCost(),tieBreaker,node)) # priority queue
				tieBreaker += 1

startingBoard = [7,2,4,5,0,6,8,3,1]

myPuzzle = Puzzle(startingBoard)
mySolver = Solver(myPuzzle)
start = time.time()
goalSeq = mySolver.AStarMT()
end = time.time()

counter = -1 # starting state doesn't count as a move
for node in goalSeq:
	counter = counter + 1
	node.puzzle.printPuzzle()
print("Total number of moves: " + str(counter))
totalTime = end - start
print("Total searching time: %.2f seconds" % (totalTime))