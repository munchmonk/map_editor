#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys
import pickle

pygame.init()

class Camera:
	def __init__(self, screen_size, map_size):
		self.pos = [0, 0]
		self.maxwidth = -(map_size[0] - screen_size[0]) if map_size[0] > screen_size[0] else 0
		self.maxheight = -(map_size[1] - screen_size[1]) if map_size[1] > screen_size[1] else 0

	def move(self, x, y):
		self.pos[0] -= x * 40
		self.pos[1] -= y * 40

		if self.pos[0] > 0:
			self.pos[0] = 0
		if self.pos[1] > 0:
			self.pos[1] = 0
		if self.pos[0] < self.maxwidth:
			self.pos[0] = self.maxwidth
		if self.pos[1] < self.maxheight:
			self.pos[1] = self.maxheight


class MapEditor:
	TILESIZE = 40
	SCREENWIDTH = TILESIZE * 15
	SCREENHEIGHT = TILESIZE * 12
	MAPWIDTH = TILESIZE * 20
	MAPHEIGHT = TILESIZE * 16

	def __init__(self):
		self.screen = pygame.display.set_mode((MapEditor.SCREENWIDTH, MapEditor.SCREENHEIGHT))
		self.my_map = pygame.Surface((MapEditor.MAPWIDTH, MapEditor.MAPHEIGHT))
		self.metadata = [[0] * (self.my_map.get_width() / MapEditor.TILESIZE) for i in range(self.my_map.get_height() / MapEditor.TILESIZE)]
		self.tiles = self.get_tiles()
		self.curr_tile = 1
		
		self.camera = Camera(self.screen.get_size(), self.my_map.get_size())

	def get_tiles(self):
		tiles = list()
		tiles.append(pygame.image.load('tile0.jpg'))
		tiles.append(pygame.image.load('tile1.jpg'))
		tiles.append(pygame.image.load('tile2.jpg'))
		return tiles

	def mouse_to_coord(self, pos):
		x, y = pos
		return (x / 40 * 40, y / 40 * 40)

	def play(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1:
						self.curr_tile = (self.curr_tile + 1) % len(self.tiles)
						if not self.curr_tile:
							self.curr_tile += 1

					elif event.key == pygame.K_k:
						pygame.image.save(self.my_map, 'map.jpeg')
						with open('metadata.p', 'wb') as out_file:
							pickle.dump(self.metadata, out_file)

					elif event.key == pygame.K_l:
						self.my_map = pygame.image.load('map.jpeg')
						with open('metadata.p', 'rb') as in_file:
							self.metadata = pickle.load(in_file)

					elif event.key == pygame.K_c:
						self.my_map = pygame.Surface((MapEditor.MAPWIDTH, MapEditor.MAPHEIGHT))
						self.metadata = [[0] * (self.my_map.get_width() / MapEditor.TILESIZE) for i in range(self.my_map.get_height() / MapEditor.TILESIZE)]

					elif event.key == pygame.K_w:
						self.camera.move(0, -1)

					elif event.key == pygame.K_a:
						self.camera.move(-1, 0)

					elif event.key == pygame.K_s:
						self.camera.move(0, 1)

					elif event.key == pygame.K_d:
						self.camera.move(1, 0)

				elif event.type == pygame.MOUSEBUTTONDOWN:
					coord = list(pygame.mouse.get_pos())
					coord[0] -= self.camera.pos[0]
					coord[1] -= self.camera.pos[1]
					coord = self.mouse_to_coord(coord)

					if event.button == 1:	
						self.my_map.blit(self.tiles[self.curr_tile], coord)
						x = coord[0] / 40
						y = coord[1] / 40
						self.metadata[y][x] = self.curr_tile

					elif event.button == 3:
						self.my_map.blit(self.tiles[0], coord)
						x = coord[0] / 40
						y = coord[1] / 40
						self.metadata[y][x] = 0
					
			self.screen.blit(self.my_map, self.camera.pos)

			coord = list(pygame.mouse.get_pos())
			coord = self.mouse_to_coord(coord)

			self.screen.blit(self.tiles[self.curr_tile], coord)

			pygame.display.flip()


if __name__ == '__main__':
	MapEditor().play()