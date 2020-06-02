############################################################

# nonogram solver

############################################################

import copy

# 10 x 10 game
x = [[1], [1, 3, 3], [2, 7], [2, 3], [2, 7], [1, 8], [5, 4], [3], [1], [2]]
y = [[6], [3, 1], [1, 2], [2, 3], [6], [4], [5], [2, 4], [2, 4, 1], [3, 6]]

# 15 x 15 game
x1 = [[3, 2, 1], [3, 1, 1, 1], [2, 1, 2, 2], [3, 5, 1], [3, 1, 1, 1], [1, 3, 2, 2], [2, 6, 1], [1, 3, 1, 1], [1, 2, 3, 3], [1, 3, 8], [2, 1, 8], [1, 5, 3], [2, 2, 3], [4, 3], [6]]
y1 = [[5], [3, 3], [2, 2], [3, 3, 1], [3, 2, 2], [2, 1, 1, 4], [2, 2, 1, 1], [1, 2, 3, 4, 1], [1, 7, 1], [14], [1, 2, 2, 3, 2], [1, 1, 1, 2, 1], [2, 2, 5], [1, 1, 4], [2, 2, 6]]

class NonogramSolver(object):

	def __init__(self, x, y):
		self.x = x
		self.y = y

		# assuming square board
		self.dim = len(x)

        # initialize board
        # 0 = unassigned, 1 = 'x', 2 = 'o'
		self.board = [0] * self.dim
		for i in range(self.dim):
			self.board[i] = [0] * self.dim

		# initialize all possible combos
		self.x_combo = [0] * len(self.x)
		self.y_combo = [0] * len(self.y)

		for i in range(self.dim):
			self.x_combo[i] = self.combo_finder(x[i], [])
			self.y_combo[i] = self.combo_finder(y[i], [])

	def combo_finder(self, x, c):
		if len(x) == 0:
			return [c + ([1] * (self.dim - len(c)))]

		guarenteed_num = sum(x) + len(x) - 1
		unknown_num = self.dim - len(c) - guarenteed_num

		combos = []

		for i in range(unknown_num + 1):
			c_copy = copy.deepcopy(c)
			c_copy += ([1] * i) + ([2] * x[0])
			if len(c_copy) != 10: 
				c_copy += [1]

			combos += self.combo_finder(x[1:], c_copy)

		return combos

	def solve(self):
		see_progression = False
		count = 0

		while  not self.is_solved():
			self.reduce()
			count += 1

			if see_progression :
				self.print_board()
				print(('-' * (self.dim + int(self.dim/5))))

		print('solved! cycles took: ', count)
		self.print_board()

	def reduce(self):
		x_commons = [0] * self.dim
		y_commons = [0] * self.dim

		for i in range(self.dim):
			x_commons[i] = self.find_common(self.x_combo[i])
			y_commons[i] = self.find_common(self.y_combo[i])

		self.update_board(x_commons, y_commons)
		self.update_combos()

	def update_combos(self):
		update_x_combos = [0] * self.dim
		update_y_combos = [0] * self.dim

		for indx in range(self.dim):
			x_indx_combos = []
			y_indx_combos = []

			for perm in self.x_combo[indx]:
				if self.is_valid(indx, True, perm):
					x_indx_combos += [perm]
			for perm in self.y_combo[indx]:
				if self.is_valid(indx, False, perm):
					y_indx_combos += [perm]

			update_x_combos[indx] = x_indx_combos
			update_y_combos[indx] = y_indx_combos

		self.x_combo = update_x_combos
		self.y_combo = update_y_combos

	def is_valid(self, i, is_row, r):
		for j in range(self.dim):
			if is_row:
				if self.board[i][j] == 0 : continue
				if self.board[i][j] != r[j]: return False
			else:
				if self.board[j][i] == 0 : continue
				if self.board[j][i] != r[j]: return False

		return True

	def update_board(self, x_commons, y_commons):
		for i in range(self.dim):
			for j in range(self.dim):

				x = x_commons[i][j]
				y = y_commons[j][i]

				self.board[i][j] = 0 if x + y == 0 else (x or y)

	def find_common(self, combos):
		common = [0] * len(combos[0])

		for i in range(len(combos[0])):
			is_common = True
			first = combos[0][i]

			for j in range(1, len(combos)):
				if combos[j][i] != first: 
					is_common = False
					break

			if is_common:
				common[i] = first

		return common

	def is_solved(self):
		for i in range(self.dim):
			if len(self.x_combo[i]) != 1 or len(self.y_combo[i]) != 1:
				return False
		return True

	def print_board(self):
		print()
		for i in range(0, len(self.board)) :
			for j in range(0, len(self.board[i])) :
				ending = ' ' if (j + 1) % 5 == 0 else ''
				print(self.convert_int_board_assignment(self.board[i][j]), end=ending)
			print()
			if ((i + 1) % 5 == 0):
				print()

	def convert_int_board_assignment(self, i):
		if i == 0: 
			return ' '
		elif i == 1:
			return 'x'
		else:
			return 'o'

NonogramSolver(x1, y1).solve()

