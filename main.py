from OpenGL.GL import *  
from OpenGL.GLUT import *  
from OpenGL.GLU import *
from random import randint

from DrawGrams import draw_mpc, draw_mpl
  
SCREEN_W, SCREEN_H = 500, 500
cells = 10

BLOCK_SIZE_W = int(SCREEN_W/cells)
BLOCK_SIZE_H = int(SCREEN_H/cells)


map_state = set()
node_paths = []


def draw_array(aPoint):
    glPointSize(1)
    glBegin(GL_POINTS)
    for point in aPoint:
        glVertex2f(point[0],point[1])
    glEnd()

def rgb(r,g,b):
    glColor3f(r/255, g/256, b/256)

def mage_cell(x,y):
    x *= BLOCK_SIZE_W
    y *= BLOCK_SIZE_H
    return draw_rectangle(x,y,x+BLOCK_SIZE_W,y+BLOCK_SIZE_H)

def create_path(x,y,dx,dy):
    nPoints = []
    if dx > 0:
        x *= BLOCK_SIZE_W
        y *= BLOCK_SIZE_H
        nPoints.extend(fill_rectangle(x+BLOCK_SIZE_W-1,y+1,x+BLOCK_SIZE_W+2,y+BLOCK_SIZE_H-1))
    elif dx < 0:
        x -= 1
        x *= BLOCK_SIZE_W
        y *= BLOCK_SIZE_H
        nPoints.extend(fill_rectangle(x+BLOCK_SIZE_W-1,y+1,x+BLOCK_SIZE_W+2,y+BLOCK_SIZE_H-1))
    elif dy > 0:
        x *= BLOCK_SIZE_W
        y *= BLOCK_SIZE_H
        nPoints.extend(fill_rectangle(x+1,y+BLOCK_SIZE_H-1,x+BLOCK_SIZE_W-2,y+BLOCK_SIZE_H+1))
    elif dy < 0:
        y -= 1
        x *= BLOCK_SIZE_W
        y *= BLOCK_SIZE_H
        nPoints.extend(fill_rectangle(x+1,y+BLOCK_SIZE_H-1,x+BLOCK_SIZE_W-2,y+BLOCK_SIZE_H+1))
    return nPoints

    return nPoints

def fill_rectangle(x1,y1,x2,y2):
    nPoints = []
    if y2 < y1:
        y1, y2 = y2, y1
    for y in range(y1,y2+1):
        nPoints.extend(draw_mpl(x1,y,x2,y))
    return nPoints

def initMap():
    for y in range(cells):
        for x in range(cells):
                map_state.update(mage_cell(x,y))
    
    
    paths = generateMage()
    for path in paths:
        mx, my = path[0]
        dx, dy = path[1][0] - mx, path[1][1] - my
        tp = create_path(mx,my,dx,dy)
        for point in tp:
            sPoint = (point[0],point[1],1)
            if sPoint in map_state:
                res = map_state.remove(sPoint)

def ranDir():
    path = [-1,0,1]
    npath = []
    while len(npath) < 3:
        rg = len(path) - 1
        if rg >= 1:
            pos = randint(0,rg)
        else:
            pos = 0
        val = path.pop(pos)
        npath.append(val)
    return npath

def unexplored_cell(map,x,y):
    for dy in ranDir():
        for dx in ranDir():
            if dx == dy == 0 or abs(dx) == abs(dy):
                continue
            px, py = x+dx, y+dy
            if py >= len(map) or px >= len(map[py]):
                continue
            if py < 0 or px < 0:
                continue
            if map[px][py] == 0:
                return (x+dx,y+dy)
            

def generateMage():
    map = [[0] * cells for _ in range(cells)]
    np = (0,0)
    paths = []
    stack = []
    points = []
    while True:
        map[np[0]][np[1]] = 1
        cp = np[:]
        points.append(cp)
        np = unexplored_cell(map,np[0],np[1])
        if np is not None:
            stack.append((cp,np))
            paths.append((cp,np))
        while np is None and len(stack) > 0:
            np = stack.pop()[0]
            continue
        if np is None:
            break
    node_paths.clear()
    node_paths.extend(paths)
    return paths

def draw_rectangle(x1,y1,x2,y2):
    nPoints = []
    nPoints.extend(draw_mpl(x1,y1,x1,y2))
    nPoints.extend(draw_mpl(x1,y1,x2,y1))
    nPoints.extend(draw_mpl(x2,y2,x2,y1))
    nPoints.extend(draw_mpl(x2,y2,x1,y2))
    return nPoints
  
def iterate():  
    glViewport(0, 0, SCREEN_W, SCREEN_H)  
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    glOrtho(0.0, SCREEN_W+cells/10, 0.0, SCREEN_H+cells/10, 0.0, 1.0)  
    glMatrixMode (GL_MODELVIEW)  
    glLoadIdentity()  
  
def showScreen():  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    glLoadIdentity()  
    iterate() 

    rgb(255,255,255)
    draw_array(map_state)
    

    glutSwapBuffers()  
    glutPostRedisplay()

def animate():
    pass

initMap()

glutInit()  
glutInitDisplayMode(GLUT_RGBA)  
glutInitWindowSize(SCREEN_W, SCREEN_H)  
glutInitWindowPosition(0, 0)  
wind = glutCreateWindow("Mank")  
glutDisplayFunc(showScreen)  
glutIdleFunc(animate)  
glutMainLoop()  
#generateMage()
#print(ranDir())