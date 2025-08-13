circleArr:list[tuple[float,float]] = []

colorLike = tuple[int,int,int]|tuple[int,int,int,int]|list[int]

posLike = tuple[float,float]|list[float]
posIntLike = tuple[int,int]|list[int]
rectLike = tuple[float,float,float,float]|list[float]

from math import sin,cos,radians

for i in range(0,360,10):
    circleArr.append((sin(radians(i)),cos(radians(i))))