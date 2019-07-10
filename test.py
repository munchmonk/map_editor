#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
# coding: utf-8

import pygame
import os
import sys


old = [0, 1, 2, 3]
new = [5, 7, 3, 3, 7, 8, 6, 1]
diff = len(new) - len(old)
tent = new[:-diff]
print(tent)

