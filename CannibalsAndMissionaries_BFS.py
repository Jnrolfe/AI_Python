#!usr/bin/env python
"""
@Author: James Rolfe
@Date: 11 November 2015
@File: CannibalsAndMissionaries_BFS.py
@Purpose: This python program will perform breadth first search to find a solution to the cannibals
			and missionaries problem. Everything is hardcoded in so all you need to do is run it 'python CannibalsAndMissionaries_BFS' 
			--created using python3.4.3
"""
import collections
import time

class Node:

	def __init__(self, cLeft, mLeft, boat, cRight, mRight, last=None):
		self.cLeft = cLeft
		self.mLeft = mLeft
		self.boat = boat
		self.cRight = cRight
		self.mRight = mRight
		self.last = last

	@property
	def isSolved(self):
		return self.cLeft == 0 and self.mLeft == 0

	@property
	def isValid(self): # rule to make sure there is never more cannibals than missionaries in one location
		return (self.mLeft >= 0 and self.mRight >= 0 \
			and self.cLeft >= 0 and self.cRight >= 0 \
			and (self.mLeft == 0 or self.mLeft >= self.cLeft) \
			and (self.mRight == 0 or self.mRight >= self.cRight))

	@property
	def state(self):
		state = [self.cLeft, self.mLeft, self.boat, self.cRight, self.mRight]
		return str(state)
	
	@property
	def seq(self): # to keep track of the sequence used to get to the goal
		node, seq = self, []
		while node:
			seq.append(node)
			node = node.last
		yield from reversed(seq)

def findMoves(node):
	moves = []
	if node.boat == 0: # means the boat is left
		# 2 m cross from left to right
		newNode = Node(node.cLeft, node.mLeft - 2, 1, node.cRight, node.mRight + 2, node)
		if newNode.isValid: # make sure move isn't illegal
			moves.append(newNode)
		# 2 c cross from left to right
		newNode = Node(node.cLeft - 2, node.mLeft, 1, node.cRight + 2, node.mRight, node)
		if newNode.isValid: 
			moves.append(newNode)
		# 1 m and 1 c cross left to right
		newNode = Node(node.cLeft - 1, node.mLeft - 1, 1, node.cRight + 1, node.mRight + 1, node)
		if newNode.isValid: 
			moves.append(newNode)
		# 1 m cross left to right
		newNode = Node(node.cLeft, node.mLeft - 1, 1, node.cRight, node.mRight + 1, node)
		if newNode.isValid: 
			moves.append(newNode)
		# 1 c cross left to right
		newNode = Node(node.cLeft - 1, node.mLeft, 1, node.cRight + 1, node.mRight, node)
		if newNode.isValid: 
			moves.append(newNode)
	else: # means the boat is right
		# 2 m cross right to left
		newNode = Node(node.cLeft, node.mLeft + 2, 0, node.cRight, node.mRight - 2, node)
		if newNode.isValid: 
			moves.append(newNode)
		# 2 c cross right to left
		newNode = Node(node.cLeft + 2, node.mLeft, 0, node.cRight - 2, node.mRight, node)
		if newNode.isValid: 
			moves.append(newNode)
		# 1 m and 1 c cross right to left
		newNode = Node(node.cLeft + 1, node.mLeft + 1, 0, node.cRight - 1, node.mRight - 1, node)
		if newNode.isValid: 
			moves.append(newNode)
		# 1 m cross right to left
		newNode = Node(node.cLeft, node.mLeft + 1, 0, node.cRight, node.mRight - 1, node)
		if newNode.isValid: 
			moves.append(newNode)
		# 1 c cross right to left
		newNode = Node(node.cLeft + 1, node.mLeft, 0, node.cRight - 1, node.mRight, node)
		if newNode.isValid: 
			moves.append(newNode)
	return moves

def BFS():
	startNode = Node(3,3,0,0,0) # start state hardcoded
	myQueue = collections.deque([startNode]) # queue for BFS
	visited = set() # don't get caught in loop
	visited.add(myQueue[0].state)
	while myQueue:
		currentNode = myQueue.pop()
		if currentNode.isSolved:
			return currentNode.seq # return sequence
		for move in findMoves(currentNode):
			nextNode = move

			if nextNode.state not in visited:
				myQueue.appendleft(nextNode)
				visited.add(nextNode.state)

def printPuzzle(goalSeq):
	counter = -1 # first state doesn't count
	for node in goalSeq:
		counter += 1
		x = node.state
		if x[2] == '0':
			x[2] = 'boat left'
		elif x[2] == '1':
			x[2] = 'boat right'
		print(x)
	print()
	print('Total moves: '+str(counter))
	return

start = time.time()
goalSeq = BFS()
end = time.time()
print('Solution in format: [cannibals on left, missionaries on left, boat position, cannibals on right, missionaries on right]\n')
printPuzzle(goalSeq)
totalTime = end - start
print("Total search time %.2f" % totalTime) 