#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
# coding: utf-8

import pygame
import os

# img_path = os.path.join("tileset1", "tile1.jpg")
# folder_path = os.path.dirname(__file__)
# tot_path = os.path.join(folder_path, img_path)
# print(tot_path)
# img = pygame.image.load(tot_path)
# target_path = os.path.join("assets", "tilesets")
# folder_path = os.path.dirname(__file__)
# target_path = "tilesets"
# final_path = os.path.join(folder_path, target_path)
# walker = os.walk(os.path.join(os.path.dirname(__file__), "tilesets"))
# walker = os.walk(final_path)
# l = [x[0] for x in walker]
# l = [x[0] for x in walker if x[0][0:4] != './.g']
# print(l)

tilesets = list()
folder_path = os.path.dirname(__file__)
target_path = "tilesets"
tilesets_path = os.path.join(folder_path, target_path)

subfolders = [x[0] for x in os.walk(tilesets_path)]

for subfolder in subfolders:
	tileset = list()
	tiles = [tile for tile in os.listdir(subfolder) if tile[-4:] == '.jpg']
	for tile in tiles:
		tileset.append(pygame.image.load(os.path.join(subfolder, tile)))
	if tileset:
		tilesets.append(tileset)

print(tilesets)

# print(l[1])
# tiles = [tile for tile in os.listdir(l[1]) if tile[-4:] == '.jpg']
# print(os.listdir(l[1]))
# print(tiles)

# for tileset in l:
#	print(tileset)
#	tiles = [tile for tile in os.listdir(tileset) if tile[-4:] == '.jpg']
#	print(tiles)
#	new_path = os.path.join(final_path, tileset)
#	print(new_path)
#	print(tileset)
#	for tile in tiles:
#		a = pygame.image.load(os.path.join(tileset, tile))
		# a = pygame.image.load(os.path.join(final_path, tile))
	# print([tile for tile in os.listdir(l[1]) if tile[-4:] == '.jpg'])












