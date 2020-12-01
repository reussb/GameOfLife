import pygame
import numpy as np

from numba import jit, cuda, uint8

TPB = 32

@cuda.jit('uint8(uint8[:,:], uint8, uint8)', device = True)
def calc_neighbors(layout, row, col):
	topLeft = 0
	topCenter = 0
	topRight = 0
	left = 0
	right = 0
	bottomLeft = 0
	bottomCenter = 0
	bottomRight = 0

	if row - 1 >= 0 and col - 1 >= 0: 
		topLeft = layout[row - 1, col - 1]

	if row - 1 >= 0:
		topCenter = layout[row - 1, col]

	if row - 1 >= 0 and col + 1 < layout.shape[1]:
		topRight = layout[row - 1, col + 1]

	if col - 1 >= 0:
		left = layout[row, col - 1]

	if col + 1 < layout.shape[1]:
		right = layout[row, col + 1]

	if col - 1 >= 0 and row + 1 < layout.shape[0]:
		bottomLeft = layout[row + 1, col - 1]

	if row + 1 < layout.shape[0]:
		bottomCenter = layout[row + 1, col]

	if row + 1 < layout.shape[0] and col + 1 < layout.shape[1]:
		bottomRight = layout[row + 1, col + 1]

	return topLeft + topCenter \
	               + topRight \
	               + left \
	               + right \
	               + bottomLeft \
	               + bottomCenter \
	               + bottomRight


@cuda.jit('void(uint8[:,:], uint8[:,:])')
def compute_next_layout(layout, next_layout):
	startX, startY = cuda.grid(2)

	gridX = cuda.gridDim.x * cuda.blockDim.x
	gridY = cuda.gridDim.y * cuda.blockDim.y

	for x in range(startX, layout.shape[1], gridX):
		for y in range(startY, layout.shape[0], gridY):
			num_neighbors = calc_neighbors(layout, y, x)

			# 1. Any live cell with fewer than two live neighbors dies
			if layout[y, x] == 1 and num_neighbors < 2:
				next_layout[y, x] = 0

			# 2. Any live cell with two or three live neighbors lives 
			elif layout[y, x] == 1 and (num_neighbors == 2 or num_neighbors == 3):
				next_layout[y, x] = 1

			# 3. Any live cell with more than three live neighbors dies
			elif layout[y, x] == 1 and num_neighbors > 3:
				next_layout[y, x] = 0

			# 4. Any dead cell with exactly three live neighbors becomes alive
			elif layout[y, x] == 0 and num_neighbors == 3:
				next_layout[y, x] = 1

			else:
				next_layout[y, x] = 0


@cuda.jit('void(uint8[:,:], uint8[:,:])')
def update_layout(layout, next_layout):
	startX, startY = cuda.grid(2)

	gridX = cuda.gridDim.x * cuda.blockDim.x
	gridY = cuda.gridDim.y * cuda.blockDim.y

	for x in range(startX, layout.shape[1], gridX):
		for y in range(startY, layout.shape[0], gridY):
			layout[y, x] = next_layout[y, x]


class GameBoard():
	def __init__(self):
		# Ensures that we can replicate the same
		# gameboard over multiple program runs
		np.random.seed(1)
		self.layout = np.random.randint(2, size = (100, 100))
		self.next_layout = np.zeros((100, 100), dtype = np.uint8)


	def update(self):
		blockdim = (32, 8)
		griddim = (32, 16)

		dev_layout = cuda.to_device(self.layout)
		dev_next_layout = cuda.to_device(self.next_layout)

		compute_next_layout[griddim, blockdim](dev_layout, dev_next_layout)
		update_layout[griddim, blockdim](dev_layout, dev_next_layout)

		dev_layout.to_host()
		dev_next_layout.to_host()


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
