#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys

pygame.init()

pygame.display.set_mode((500, 500))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			print(event.button)