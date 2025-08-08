from Engine.Vec3 import Vec3

from Engine.Constants import colorLike

def loadObject0(path,scale:float=1)->tuple[list[Vec3],list[list[int]],list[list[float]]]:
    with open(path) as file:
        file = file.read()
        file = file.split('\n')
        
        points = [i for i in file if i.startswith('v ')]
        faces = [i for i in file if i.startswith('f ')]
        faceNormals = [i for i in file if i.startswith('vn ')]

    points = [i.split() for i in points][1:]
    points = [[float(j) for j in i] for i in points]

    points = [Vec3(*point) for point in points]
    
    points = [point*Vec3(scale,-scale,scale) for point in points]

    faces = [i[2:] for i in faces]
    faces = [i.split(' ') for i in faces]
    faces = [[int(j[:j.index('/')])-1 for j in i] for i in faces]

    faceNormals = [i[3:] for i in faceNormals]
    faceNormals = [i.split(' ') for i in faceNormals]
    faceNormals = [[float(j) for j in i] for i in faceNormals]
    faceNormals = [[-i[0],i[1],-i[2]] for i in faceNormals]
    
    return points,faces,faceNormals

def loadObject(path:str,position:Vec3=Vec3(),scale:float|Vec3=1,angle=Vec3())->list['Triangle']:
    with open(path) as file:
        file = file.read()
        file = file.split('\n')
        
        points = [i for i in file if i.startswith('v ')]
        faceIndexes = [i for i in file if i.startswith('f ')]
        vertexNormals = [i for i in file if i.startswith('vn ')]

    points = [i.split()[1:] for i in points]
    points = [[float(j) for j in i] for i in points]

    points = [Vec3(point[0],-point[1],point[2]) for point in points]
    
    points = [Vec3.rotate(point,angle) for point in points]
    
    points = [point*scale for point in points]
    points = [point+position for point in points]

    vertexNormals = [i.split()[1:] for i in vertexNormals]
    vertexNormals = [[float(j) for j in i] for i in vertexNormals]
    vertexNormals = [Vec3(*normals) for normals in vertexNormals]

    vertexNormals = [Vec3.rotate(normal,angle) for normal in vertexNormals]
    vertexNormals = [(normal*scale).normalized() for normal in vertexNormals]
    
    faceIndexes = [i[2:] for i in faceIndexes]
    faceIndexes = [i.split(' ') for i in faceIndexes]
    faceNormals:list[Vec3] = []
    
    normalIndexes = [int(i[0][i[0].index('/')+2:])-1 for i in faceIndexes]
    faceNormals = [vertexNormals[i] for i in normalIndexes]
    faceIndexes = [[int(j[:j.index('/')])-1 for j in i] for i in faceIndexes]

    faces:list[tuple[Vec3,Vec3,Vec3]] = []
    for i0,i1,i2 in faceIndexes:
        # faceNormals.append((vertexNormals[i0]+vertexNormals[i1]+vertexNormals[i2]).normalized())
        faces.append((points[i0],points[i1],points[i2]))
    
    triangles = [Triangle(f,n) for f,n in zip(faces,faceNormals)]

    # boundingBoxMin = Vec3(min([p.x for p in points]),min([p.y for p in points]),min([p.z for p in points]))
    # boundingBoxMax = Vec3(max([p.x for p in points]),max([p.y for p in points]),max([p.z for p in points]))
    return triangles

class Object3D:
    def __init__(self,path:str,color:tuple[float,float,float],pos:Vec3=Vec3(),scale:float|Vec3=1,angle=Vec3()):
        self.triangles:list[Triangle] = loadObject(path,pos,scale,angle)

        self.color = color

class Triangle:
    def __init__(self,p:tuple[Vec3,Vec3,Vec3],normal:Vec3):
        self.a = p[0]
        self.b = p[1]
        self.c = p[2]
        self.normal = normal
    
    def __str__(self):
        return f'Triangle({self.a},{self.b},{self.c},{self.normal})'
    def __repr__(self):
        return f'Triangle({self.a},{self.b},{self.c},{self.normal})'
    def __iter__(self):
        return iter((self.a,self.b,self.c))
    
    def boundingBox(self):
        Min = Vec3(min([p.x for p in self]),min([p.y for p in self]),min([p.z for p in self]))
        Max = Vec3(max([p.x for p in self]),max([p.y for p in self]),max([p.z for p in self]))
        return Min,Max

class Cam3D:
    def __init__(self,angle:Vec3,pos:Vec3,zNear:float,zFar:float,FOV:float):
        self.dir = angle
        self.pos = pos
        
        self.zNear = zNear
        self.zFar = zFar

        self.FOV = FOV

import math

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def avg(l):
    l2 = len(l)
    return [sum([i[j] for i in l])/l2 for j in range(len(l[0]))]

def rotate(point,angle:Vec3,offset=[0,0,0]):
    x,y,z = point
    
    x -= offset.x
    y -= offset.y
    z -= offset.z
    
    #y
    x,z = x*cos(angle.y)-z*sin(angle.y),x*sin(angle.y)+z*cos(angle.y)
    
    #x
    y,z = y*cos(angle.x)-z*sin(angle.x),y*sin(angle.x)+z*cos(angle.x)
    
    #z
    x,y = x*cos(angle.z)-y*sin(angle.z),x*sin(angle.z)+y*cos(angle.z)
    
    # x += offset.x
    # y += offset.y
    # z += offset.z
    
    return x,y,z

def plot(point,m,zNear,zFar,FOV):
    x,y,z = point
    
    x1 = 1/(tan(FOV/2))*x
    y1 = 1/(tan(FOV/2))*y
    z1 = (zFar+zNear)/(zNear-zFar)*z+(2*zFar*zNear)/(zNear-zFar)
    w1 = -z
    
    w1 = max(w1,0.01)
    
    x1 /= w1
    y1 /= w1
    
    x1 *= m
    y1 *= m
    
    return (x1,y1) if z1 >= 0 else (0,0)

def offset(point,mid):
    return (point[0]+mid[0],point[1]+mid[1])

def moveF(angle,speed:float):
    '''Motion based on direction'''
    yaw, pitch = angle.y,angle.x
    
    # yaw = math.radians(yaw)
    # pitch = math.radians(pitch)
    
    forward_x = 0
    forward_y = 0
    forward_z = 0
    
    forward_x = -sin(yaw)*cos(pitch)
    forward_y = -sin(pitch)
    forward_z = -cos(yaw)*cos(pitch)
    
    return Vec3(forward_x*speed,forward_y*speed,forward_z*speed)

def moveF2(angle,speed:float):
    '''Move in XY, locked Z'''
    
    yaw = angle.y
    
    forward_x = 0
    forward_y = 0
    forward_z = 0
    
    forward_x = -sin(yaw)
    forward_z = -cos(yaw)
    
    return Vec3(forward_x*speed,forward_y*speed,forward_z*speed)

def moveR(angle,speed:float):
    '''Move right based on direction'''
    
    yaw = angle.y+90
    
    forward_x = 0
    forward_y = 0
    forward_z = 0
    
    forward_x = sin(yaw)
    forward_z = cos(yaw)
    
    return Vec3(forward_x*speed,forward_y*speed,forward_z*speed)

# def normalize(v):
#     divide = math.dist(v,(0,0,0))
#     if divide == 0:
#         return [0,0,0]
#     return [v[0]/divide,v[1]/divide,v[2]/divide]

# def getNormal(face):
#     if len(face) <= 2:
#         return [0,0,0]
    
#     A = face[1]-face[0]
#     B = face[2]-face[0]

#     nx = A[1]*B[2]-A[2]*B[1]
#     ny = A[2]*B[0]-A[0]*B[2]
#     nz = A[0]*B[1]-A[1]*B[0]
    
#     return normalize([nx,ny,nz])

# def cast(p,angle,height):
#     direction = moveF(angle)
        
#     x,y,z = p
    
#     dx,dy,dz = direction
    
#     if dy == 0 or (angle[1]+90)%360 >= 180:
#         return (0,0,0)

#     t = (height-y)/dy
    
#     ix = x+t*dx
#     iy = y+t*dy
#     iz = z+t*dz
    
#     return (ix,iy,iz)

# def clockwise(polygon):
#     s = 0
#     for i in range(len(polygon)-1):
#         s += (polygon[i][0]-polygon[i+1][0])*(polygon[i][1]+polygon[i+1][1])
#     s += (polygon[0][0]-polygon[-1][0])*(polygon[0][1]+polygon[-1][1])
    
#     return s >= 0