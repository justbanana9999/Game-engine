from Engine.All import *

file = File('File.test')

pos,size = file.load()

file.save(pos,size)
