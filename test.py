#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
# coding: utf-8

import pygame
import os
import sys


pygame.init()

s = pygame.display.set_mode((500, 500))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	print(pygame.mouse.get_focused())
