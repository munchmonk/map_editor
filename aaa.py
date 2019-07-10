#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
# coding: utf-8

""" 
	dynamically enlarge/shrink map
	tag metadata (e.g. WALKABLE, OBSTACLE, etc.)
	potentially let user add metadata only (over existing tiles)
	load tilesets from different folders
	tile randomiser among tileset
"""

import pygame
import sys
import pickle


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

	def apply_to_coord(self, coord):
		return coord[0] - self.pos[0], coord[1] - self.pos[1]

	def get_pos(self):
		return self.pos


class Util:
	def __init__(self):
		pass

	def round_down_coords(self, coord):
		# Rounds down coordinates to the nearest TILESIZE
		return (coord[0] / MapEditor.TILESIZE * MapEditor.TILESIZE, coord[1] / MapEditor.TILESIZE * MapEditor.TILESIZE)

	def coord_to_index(self, coord):
		# Converts coordinates to indexes
		return coord[0] / MapEditor.TILESIZE, coord[1] / MapEditor.TILESIZE

	def get_tiles(self):
		tiles = list()
		tiles.append(pygame.image.load('tile0.jpg'))
		tiles.append(pygame.image.load('tile1.jpg'))
		tiles.append(pygame.image.load('tile2.jpg'))
		return tiles


class MapEditor:
	TILESIZE = 40
	SCREENWIDTH = TILESIZE * 5
	SCREENHEIGHT = TILESIZE * 5
	MAPWIDTH = TILESIZE * 4
	MAPHEIGHT = TILESIZE * 4
	FPS = 90

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((MapEditor.SCREENWIDTH, MapEditor.SCREENHEIGHT))
		# self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		
		self.util = Util()
		
		self.my_map = pygame.Surface((MapEditor.MAPWIDTH, MapEditor.MAPHEIGHT))
		self.metadata = [[0] * (self.my_map.get_width() / MapEditor.TILESIZE) for i in range(self.my_map.get_height() / MapEditor.TILESIZE)]
		self.tiles = self.util.get_tiles()
		self.curr_tile = 1

		self.camera = Camera(self.screen.get_size(), self.my_map.get_size())
		self.clock = pygame.time.Clock()

	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				# ESC - exit program
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

				# 1 - change tile
				elif event.key == pygame.K_1:
					self.curr_tile = (self.curr_tile + 1) % len(self.tiles)
					if not self.curr_tile:
						self.curr_tile += 1

				# K - save
				elif event.key == pygame.K_k:
					pygame.image.save(self.my_map, 'map.jpeg')
					with open('metadata.p', 'wb') as out_file:
						pickle.dump(self.metadata, out_file)

				# L - load
				elif event.key == pygame.K_l:
					self.my_map = pygame.image.load('map.jpeg')
					with open('metadata.p', 'rb') as in_file:
						self.metadata = pickle.load(in_file)

				# C - clear
				elif event.key == pygame.K_c:
					self.my_map = pygame.Surface((MapEditor.MAPWIDTH, MapEditor.MAPHEIGHT))
					self.metadata = [[0] * (self.my_map.get_width() / MapEditor.TILESIZE) for i in range(self.my_map.get_height() / MapEditor.TILESIZE)]

	def get_camera_movements(self):
		# WASD - move camera
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.camera.move(0, -1)
		if keys[pygame.K_a]:
			self.camera.move(-1, 0)
		if keys[pygame.K_s]:
			self.camera.move(0, 1)
		if keys[pygame.K_d]:
			self.camera.move(1, 0)

	def is_coord_within_map_bounds(self, coord):
		if coord[0] < MapEditor.MAPWIDTH and coord[1] < MapEditor.MAPHEIGHT:
			return True
		return False

	def process_mouse_clicks(self):
		# Left click - draw
		if pygame.mouse.get_pressed()[0]:
			coord = self.util.round_down_coords(self.camera.apply_to_coord(list(pygame.mouse.get_pos())))

			if not self.is_coord_within_map_bounds(coord):
				return

			self.my_map.blit(self.tiles[self.curr_tile], coord)
			x, y = self.util.coord_to_index(coord)
			self.metadata[y][x] = self.curr_tile

		# Right click - erase
		elif pygame.mouse.get_pressed()[2]:
			coord = self.util.round_down_coords(self.camera.apply_to_coord(list(pygame.mouse.get_pos())))

			if not self.is_coord_within_map_bounds(coord):
				return

			self.my_map.blit(self.tiles[0], coord)
			x, y = self.util.coord_to_index(coord)
			self.metadata[y][x] = 0

	def draw(self):
		# Draw map
		self.screen.blit(self.my_map, self.camera.get_pos())

		# Preview current tile at cursor position
		coord = self.util.round_down_coords(list(pygame.mouse.get_pos()))
		if self.is_coord_within_map_bounds(coord):
			self.screen.blit(self.tiles[self.curr_tile], coord)

		pygame.display.flip()

	def play(self):
		while True:
			self.process_events()
			self.get_camera_movements()
			self.process_mouse_clicks()				
			self.draw()
			self.clock.tick(MapEditor.FPS)


if __name__ == '__main__':
	MapEditor().play()