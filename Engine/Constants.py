circle:list[tuple[float,float]] = []

import pygame

colorLike = pygame.typing.ColorLike
posLike = pygame.typing.Point
posIntLike = pygame.typing.IntPoint
rectLike = pygame.typing.RectLike

from math import sin,cos,radians

for i in range(0,360,10):
    circle.append((sin(radians(i)),cos(radians(i))))