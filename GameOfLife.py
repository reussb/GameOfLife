#!/usr/bin/env python3

"""
The purpose of the code is to demonstrate how implementing
algorithms in numba CUDA to run on the GPU can decrease the
amount of time it takes to reach a specified board state in
Conway's "Game of Life".
"""

import time, sys, pygame

from game_board import GameBoard
from game_board_cuda import GameBoard as CudaBoard


__author__ = 'Benjamin Reuss'
__email__ = 'reussba@mail.uc.edu'


if __name__ == '__main__':
	pygame.init()
	
	game_board = GameBoard()
	cuda_board = CudaBoard()

	current_board = game_board

	update_count = 0
	start_time = None
	end_time = None

	display = pygame.display.set_mode((800, 600), 0, 32)

	while True:
		if update_count == 0:
			start_time = time.time()
			print("\nDrawing 100 iterations on CPU...")

		elif update_count == 99:
			end_time = time.time()
			print("Finished 100 iterations on CPU...")
			print("Time to finish: {} seconds".format(end_time - start_time))

		elif update_count == 100:
			start_time = time.time()
			print("\nDrawing 100 iterations on GPU with CUDA...")

		elif update_count == 199:
			end_time = time.time()
			print("Finished 100 iterations on GPU with CUDA...")
			print("Time to finish: {} seconds".format(end_time - start_time))

		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		if update_count < 100:
			game_board.update()
			current_board = game_board

		elif update_count < 200:
			cuda_board.update()
			current_board = cuda_board

		current_board.draw(display)

		pygame.display.update()

		update_count += 1