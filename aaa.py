#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys
import pickle

pygame.init()

def get_tiles():
	tiles = list()
	tiles.append(pygame.image.load('tile1.jpg'))
	tiles.append(pygame.image.load('tile2.jpg'))
	return tiles

def mouse_to_coord(pos):
	x, y = pos
	return (x / 40 * 40, y / 40 * 40)


def play():
	screen = pygame.display.set_mode((40 * 6, 40 * 4))
	my_map = pygame.Surface(screen.get_size())
	metadata = [[0] * (screen.get_width() / 40) for i in range(screen.get_height() / 40)]
	tiles = get_tiles()
	curr_tile = 0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					curr_tile = (curr_tile + 1) % len(tiles)

				elif event.key == pygame.K_s:
					pygame.image.save(my_map, 'map.jpeg')
					with open('metadata.p', 'wb') as out_file:
						pickle.dump(metadata, out_file)

				elif event.key == pygame.K_l:
					my_map = pygame.image.load('map.jpeg')
					with open('metadata.p', 'rb') as in_file:
						metadata = pickle.load(in_file)
					print(metadata)

				elif event.key == pygame.K_c:
					my_map = pygame.Surface((40 * 12, 40 * 12))
					metadata = [[0] * (screen.get_width() / 40) for i in range(screen.get_height() / 40)]
					print(metadata)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				coord = mouse_to_coord(pygame.mouse.get_pos())
				my_map.blit(tiles[curr_tile], coord)
				x = coord[0] / 40
				y = coord[1] / 40
				metadata[y][x] = curr_tile + 1
				print(metadata)

				
			
		screen.blit(my_map, (0, 0))
		pygame.display.flip()



if __name__ == '__main__':
	play()