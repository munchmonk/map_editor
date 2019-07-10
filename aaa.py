#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
# coding: utf-8

""" 
	NEXT UP:
	dynamically enlarge/shrink map

	TODO:
	potentially allow for manual metadata override
	tile randomiser among tileset
	NOTE: no sanity checks at all on metadata files for now
"""

import pygame
import sys
import pickle
import os


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

	def initialise_tilesets(self):
		tilesets = list()
		folder_path = os.path.dirname(__file__)
		target_path = 'tilesets'
		tilesets_path = os.path.join(folder_path, target_path)

		subfolders = [x[0] for x in os.walk(tilesets_path)]

		for subfolder in subfolders:

			# Skips the current folder
			if subfolder == tilesets_path:
				continue

			tileset = list()

			try:
				with open(os.path.join(subfolder, 'metadata.txt'), 'r') as metadata_file:

					for line in metadata_file:
						text = line.split()

						# Avoids empty lines
						if text:
							tileset.append(text)
						
			except IOError:
				print('Error: no metadata file for tileset {}'.format(subfolder))

			# Replaces the file names with the actual images
			for entry in tileset:
				entry[0] = pygame.image.load(os.path.join(subfolder, entry[0]))

			tilesets.append(tileset)

		return tilesets

	def initialise_blank_tile(self):
		folder_path = os.path.dirname(__file__)
		img_path = os.path.join(folder_path, "blank.jpg")
		return pygame.image.load(img_path)

	def quit(self):
		pygame.quit()
		sys.exit()

	def is_coord_within_map_bounds(self, coord):
		if coord[0] < MapEditor.MAPWIDTH and coord[1] < MapEditor.MAPHEIGHT:
			return True
		return False


class MapEditor:
	TILESIZE = 40
	SCREENWIDTH = TILESIZE * 12
	SCREENHEIGHT = TILESIZE * 12
	MAPWIDTH = TILESIZE * 40
	MAPHEIGHT = TILESIZE * 40
	FPS = 90

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((MapEditor.SCREENWIDTH, MapEditor.SCREENHEIGHT))
		# self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		
		self.util = Util()
		
		self.my_map = pygame.Surface((MapEditor.MAPWIDTH, MapEditor.MAPHEIGHT))
		self.my_metadata = [[0] * (self.my_map.get_width() / MapEditor.TILESIZE) for i in range(self.my_map.get_height() / MapEditor.TILESIZE)]

		self.tilesets = self.util.initialise_tilesets()
		self.curr_tileset_index = 0
		self.curr_tileset = self.tilesets[self.curr_tileset_index]
		self.curr_tile_index = 0
		self.curr_tile = self.curr_tileset[self.curr_tile_index][0]
		
		self.blank_tile = self.util.initialise_blank_tile()

		self.camera = Camera(self.screen.get_size(), self.my_map.get_size())
		self.clock = pygame.time.Clock()

	def next_tileset(self):
		self.curr_tileset_index = (self.curr_tileset_index + 1) % len(self.tilesets)
		self.curr_tileset = self.tilesets[self.curr_tileset_index]

		# Reset index to 0 in case new tileset is smaller than previous one - avoids index out of range
		self.curr_tile_index = 0
		self.curr_tile = self.curr_tileset[self.curr_tile_index][0]

	def prev_tileset(self):
		self.curr_tileset_index = (self.curr_tileset_index - 1) % len(self.tilesets)
		self.curr_tileset = self.tilesets[self.curr_tileset_index]

		# Reset index to 0 in case new tileset is smaller than previous one - avoids index out of range
		self.curr_tile_index = 0
		self.curr_tile = self.curr_tileset[self.curr_tile_index][0]

	def next_tile(self):
		self.curr_tile_index = (self.curr_tile_index + 1) % len(self.curr_tileset)
		self.curr_tile = self.curr_tileset[self.curr_tile_index][0]

	def prev_tile(self):
		self.curr_tile_index = (self.curr_tile_index - 1) % len(self.curr_tileset)
		self.curr_tile = self.curr_tileset[self.curr_tile_index][0]

	def save(self):
		pygame.image.save(self.my_map, os.path.join(os.path.dirname(__file__), 'map.jpeg'))
		with open(os.path.join(os.path.dirname(__file__), 'metadata.p'), 'wb') as out_file:
			pickle.dump(self.my_metadata, out_file)

	def load(self):
		self.my_map = pygame.image.load(os.path.join(os.path.dirname(__file__), 'map.jpeg'))
		with open(os.path.join(os.path.dirname(__file__), 'metadata.p'), 'rb') as in_file:
			self.my_metadata = pickle.load(in_file)

	def clear(self):
		self.my_map = pygame.Surface((MapEditor.MAPWIDTH, MapEditor.MAPHEIGHT))
		self.metadata = [[0] * (self.my_map.get_width() / MapEditor.TILESIZE) for i in range(self.my_map.get_height() / MapEditor.TILESIZE)]

	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.util.quit()

			elif event.type == pygame.KEYDOWN:
				# ESC - exit program
				if event.key == pygame.K_ESCAPE:
					self.util.quit()

				# E - next tileset
				elif event.key == pygame.K_e:
					self.next_tileset()

				# Q - prev tileset
				elif event.key == pygame.K_q:
					self.prev_tileset()

				# K - save
				elif event.key == pygame.K_k:
					self.save()

				# L - load
				elif event.key == pygame.K_l:
					self.load()

				# C - clear
				elif event.key == pygame.K_c:
					self.clear()

			# Change tiles with mousewheel
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					self.prev_tile()
				elif event.button == 5:
					self.next_tile()


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

	def process_mouse_clicks(self):
		# Left click - draw
		if pygame.mouse.get_pressed()[0]:
			coord = self.util.round_down_coords(self.camera.apply_to_coord(list(pygame.mouse.get_pos())))

			if not self.util.is_coord_within_map_bounds(coord):
				return

			self.my_map.blit(self.curr_tile, coord)
			x, y = self.util.coord_to_index(coord)
			self.my_metadata[y][x] = self.curr_tileset[self.curr_tile_index][1:]

		# Right click - erase
		elif pygame.mouse.get_pressed()[2]:
			coord = self.util.round_down_coords(self.camera.apply_to_coord(list(pygame.mouse.get_pos())))

			if not self.util.is_coord_within_map_bounds(coord):
				return

			self.my_map.blit(self.blank_tile, coord)
			x, y = self.util.coord_to_index(coord)
			self.my_metadata[y][x] = [0]

	def draw(self):
		# Draw map
		self.screen.blit(self.my_map, self.camera.get_pos())

		# Preview current tile at cursor position
		coord = self.util.round_down_coords(list(pygame.mouse.get_pos()))
		if self.util.is_coord_within_map_bounds(coord):
			self.screen.blit(self.curr_tile, coord)

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