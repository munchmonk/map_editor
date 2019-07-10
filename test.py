#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
# coding: utf-8

import pygame
import os
import sys


tiles = [tile for tile in os.listdir(subfolder) if tile[-4:] == '.jpg']