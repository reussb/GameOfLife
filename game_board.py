import pygame
import numpy as np

class GameBoard():
	def __init__(self):
		# Ensures that we can replicate the same
		# gameboard over multiple program runs
		np.random.seed(1)
		self.layout = np.random.randint(2, size = (100, 100))
		self.next_layout = np.zeros((100, 100), dtype = np.uint8)


	def update(self):
		for y in range(self.layout.shape[0]):
			for x in range(self.layout.shape[1]):
				adj = self.get_adj_cells(y, x)

				live_count = 0
				for cell in adj:
					if cell == 1:
						live_count = live_count + 1

				self.next_layout[y, x] = self.get_next_cell_state(live_count, self.layout[y, x])

		for y in range(self.layout.shape[0]):
			for x in range(self.layout.shape[1]):
				self.layout[y, x] = self.next_layout[y, x]


	def draw(self, display):
		for y in range(self.layout.shape[0]):
			for x in range(self.layout.shape[1]):
				screen_x = x / self.layout.shape[1] * display.get_width()
				screen_y = y / self.layout.shape[0] * display.get_height()
				width = display.get_width() / self.layout.shape[1]
				height = display.get_height() / self.layout.shape[0]

				if self.layout[y, x] == 0:
					pygame.draw.rect(display, (0, 0, 0), (screen_x, screen_y, width, height))
				else:
					pygame.draw.rect(display, (255, 255, 255), (screen_x, screen_y, width, height))


	def get_next_cell_state(self, num_live_adj, state):
		
		# 1. Any live cell with fewer than two live neighbors dies
		if state == 1 and num_live_adj < 2:
			return 0

		# 2. Any live cell with two or three live neighbors lives 
		elif state == 1 and (num_live_adj == 2 or num_live_adj == 3):
			return 1

		# 3. Any live cell with more than three live neighbors dies
		elif state == 1 and num_live_adj > 3:
			return 0

		# 4. Any dead cell with exactly three live neighbors becomes alive
		elif state == 0 and num_live_adj == 3:
			return 1

		return 0


	def get_adj_cells(self, y, x):
		adj_cells = []

		is_top_row = (y == 0)
		is_bottom_row = (y == self.layout.shape[0] - 1)
		is_left_col = (x == 0)
		is_right_col = (x == self.layout.shape[1] - 1)

		is_top_left_corner = (is_top_row and is_left_col)
		is_top_right_corner = (is_top_row and is_right_col)
		is_bottom_left_corner = (is_bottom_row and is_left_col)
		is_bottom_right_corner = (is_bottom_row and is_right_col)

		if is_top_left_corner:
			adj_cells.append(self.layout[y, x + 1])
			adj_cells.append(self.layout[y + 1, x])
			adj_cells.append(self.layout[y + 1, x + 1])

		elif is_top_right_corner:
			adj_cells.append(self.layout[y, x - 1])
			adj_cells.append(self.layout[y + 1, x - 1])
			adj_cells.append(self.layout[y + 1, x])

		elif is_bottom_left_corner:
			adj_cells.append(self.layout[y - 1, x])
			adj_cells.append(self.layout[y - 1, x + 1])
			adj_cells.append(self.layout[y, x + 1])

		elif is_bottom_right_corner:
			adj_cells.append(self.layout[y - 1, x - 1])
			adj_cells.append(self.layout[y - 1, x])
			adj_cells.append(self.layout[y, x - 1])

		elif is_top_row:
			adj_cells.append(self.layout[y, x - 1])
			adj_cells.append(self.layout[y, x + 1])
			adj_cells.append(self.layout[y + 1, x - 1])
			adj_cells.append(self.layout[y + 1, x])
			adj_cells.append(self.layout[y + 1, x + 1])

		elif is_bottom_row:
			adj_cells.append(self.layout[y - 1, x - 1])
			adj_cells.append(self.layout[y - 1, x])
			adj_cells.append(self.layout[y - 1, x + 1])
			adj_cells.append(self.layout[y, x - 1])
			adj_cells.append(self.layout[y, x + 1])

		elif is_left_col:
			adj_cells.append(self.layout[y - 1, x])
			adj_cells.append(self.layout[y - 1, x + 1])
			adj_cells.append(self.layout[y, x + 1])
			adj_cells.append(self.layout[y + 1, x])
			adj_cells.append(self.layout[y + 1, x + 1])

		elif is_right_col:
			adj_cells.append(self.layout[y - 1, x - 1])
			adj_cells.append(self.layout[y - 1, x])
			adj_cells.append(self.layout[y, x - 1])
			adj_cells.append(self.layout[y + 1, x - 1])
			adj_cells.append(self.layout[y + 1, x])

		else:
			adj_cells.append(self.layout[y - 1, x - 1])
			adj_cells.append(self.layout[y - 1, x])
			adj_cells.append(self.layout[y - 1, x + 1])
			adj_cells.append(self.layout[y, x - 1])
			adj_cells.append(self.layout[y, x + 1])
			adj_cells.append(self.layout[y + 1, x - 1])
			adj_cells.append(self.layout[y + 1, x])
			adj_cells.append(self.layout[y + 1, x + 1])

		return adj_cells
