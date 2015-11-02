'''
File:
	ChessBoard.py
Author:
 	James Rolfe
Date: 
	31 October 2015
Purpose:
	Be given a list of coordinates and print out a corresponding board
'''

'''
for i in range(8):
	for j in range(8):
		if j < 7:
			print('. ', end="")
		else:
			print('.')
'''

class ChessBoard:
	def __init__(self, start=0):
		self.board = [['.','.','.','.','.','.','.','.'],\
						['.','.','.','.','.','.','.','.'],\
						['.','.','.','.','.','.','.','.'],\
						['.','.','.','.','.','.','.','.'],\
						['.','.','.','.','.','.','.','.'],\
						['.','.','.','.','.','.','.','.'],\
						['.','.','.','.','.','.','.','.'],\
						['.','.','.','.','.','.','.','.']]
		if start == 0:
			self.board[0] = ['c','n','b','q','k','b','n','c']
			self.board[1] = ['p','p','p','p','p','p','p','p']
			self.board[2] = ['.','.','.','.','.','.','.','.']
			self.board[3] = ['.','.','.','.','.','.','.','.']
			self.board[4] = ['.','.','.','.','.','.','.','.']
			self.board[5] = ['.','.','.','.','.','.','.','.']
			self.board[6] = ['P','P','P','P','P','P','P','P']
			self.board[7] = ['C','N','B','Q','K','B','N','C']

	def getState(self):
		return self.board

	def printBoard(self):
		b = self.getState()
		for i in range(8):
			for j in range(8):
				print(b[i][j] + ' ', end="")
			print()

	def move(self, moveCoor):
		from_row = moveCoor[0][0]
		from_col = moveCoor[0][1]
		to_row = moveCoor[1][0]
		to_col = moveCoor[1][1]

		self.board[to_row][to_col] = self.board[from_row][from_col]
		self.board[from_row][from_col] = '.'

# testing
cb = ChessBoard(0)
cb.printBoard()
print()
cb.move(((0,0),(3,2)))
cb.printBoard()