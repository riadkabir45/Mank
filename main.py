from OpenGL.GL import *  
from OpenGL.GLUT import *  
from OpenGL.GLU import *
from random import randint
from math import sin,pi,cos,sqrt,atan2,degrees,radians

from DrawGrams import draw_mpc, draw_mpl
from angler import differ as angDir

SCREEN_W, SCREEN_H = 2*500, 2*500
DPI = (SCREEN_W//500,SCREEN_H//500)
cells = 20
rotation_speed = 5

BLOCK_SIZE_W = round(SCREEN_W/cells)
BLOCK_SIZE_H = round(SCREEN_H/cells)


map_state = set()
node_paths = []

bullets = []
entity = []

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
        nPoints.extend(fill_rectangle(x+1,y+BLOCK_SIZE_H-1,x+BLOCK_SIZE_W-1,y+BLOCK_SIZE_H+1))
    elif dy < 0:
        y -= 1
        x *= BLOCK_SIZE_W
        y *= BLOCK_SIZE_H
        nPoints.extend(fill_rectangle(x+1,y+BLOCK_SIZE_H-1,x+BLOCK_SIZE_W-1,y+BLOCK_SIZE_H+1))
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

def translate(points,x,y):
    for point in points:
        point[0] += x
        point[1] += y

def rotate(points,angle):
    rad = (angle*(2*pi/360))
    for point in points:
        x, y, g = point
        point[0] = x*cos(rad) - y*sin(rad)
        point[1] = x*sin(rad) + y*cos(rad)
    #print(sin(angle*(2*pi/360)))

def mid_point(x,y):
    return (BLOCK_SIZE_W*(x)+BLOCK_SIZE_W//2,BLOCK_SIZE_H*(y)+BLOCK_SIZE_H//2)

def mutate(points):
    for i in range(len(points)):
        points[i] = list(points[i])

class GameObject:
    def transform(self,points):
        x, y = self.x, self.y
        mutate(points)
        translate(points,-x,-y)
        rotate(points,self.angle)
        translate(points,x,y)
    
    def corners(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        return ((x-w//2,y-h//2),(x-w//2,y+h//2),(x+w//2,y-h//2),(x+w//2,y+h//2),)
    
    def check_collision(self):
        for  ob in entity:
            if ob != self.owner:
                print(ob.corners(),ob,self.corners(),self)
                for corn in self.corners():
                    mcorn = ob.corners()
                    x1, y1 = mcorn[0]
                    x2, y2 = mcorn[3]
                    if x1 <= corn[0] <= x2 and y1 <= corn[1] <= y2:
                        return ob

    def move(self,d,speed = rotation_speed):
        if d == 'a':
            self.angle += speed
            if self.angle >= 360:
                self.angle = 0
            return False

        if d == 'd':
            self.angle -= speed
            if self.angle < 0:
                self.angle = 359
            return False
        x, y, w, h = self.x, self.y, self.w, self.h
        ox, oy = x, y
        tx, ty = x, y
        rcollision = False
        dist = 0
        while dist <= speed:
            y = oy
            if d == "w":
                y += round(dist*sin(self.angle*(2*pi/360)))
            elif d == "s":
                y -= round(dist*sin(self.angle*(2*pi/360)))
            borderPoint = []
            borderPoint.extend(draw_rectangle(x-w//2,y-h//2,x+w//2,y+h//2))
            borderPoint.extend(draw_rectangle(x-w//6,y-h//6,x+w*4//5,y+h//6))
            collision = False
            for point in borderPoint:
                if point in map_state:
                    collision = not collision
                    rcollision = True
                    break
            if collision:
                break
            dist += 1
            ty = y

        dist = 0
        while dist <= speed:
            x = ox
            if d == "w":
                x += round(dist*cos(self.angle*(2*pi/360)))
            elif d == "s":
                x -= round(dist*cos(self.angle*(2*pi/360)))
            borderPoint = []
            borderPoint.extend(draw_rectangle(x-w//2,y-h//2,x+w//2,y+h//2))
            borderPoint.extend(draw_rectangle(x-w//6,y-h//6,x+w*4//5,y+h//6))
            collision = False
            for point in borderPoint:
                if point in map_state:
                    collision = not collision
                    rcollision = True
                    break
            if collision:
                break
            dist += 1
            tx = x

        self.x = tx
        self.y = ty
        return rcollision
    

class Bullet(GameObject):
    def __init__(self,x,y,angle,owner):
        bullets.append(self)
        self.x, self.y = x, y
        self.angle = angle
        self.w = 5*DPI[0]
        self.h = 2*DPI[0]
        self.owner = owner
    
    def move(self):
        x, y = self.x, self.y
        state = super().move('w')
        return state

    
    def draw(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        borderPoint = []
        bodyPoint = []
        rgb(153, 77, 55)
        bodyPoint.extend(fill_rectangle(x-w//2,y-h//2,x+w//2,y+h//2))

        self.transform(bodyPoint)

        draw_array(bodyPoint)

        rgb(255, 255, 255)
        borderPoint.extend(draw_rectangle(x-w//2,y-h//2,x+w//2,y+h//2))

        self.transform(borderPoint)

        draw_array(borderPoint)
    
    def destroy(self):
        bullets.remove(self)

class Tank(GameObject):
    def __init__(self,x,y,w=10,h=10):
        self.w,self.h = 10*DPI[0],10*DPI[1]
        self.x, self.y = x, y
        self.angle = 90
        self.target = None
        entity.append(self)

    def fire(self):
        Bullet(self.x,self.y,self.angle,self)
    
    def draw(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        borderPoint = []
        bodyPoint = []
        
        rgb(153, 77, 55)
        bodyPoint.extend(fill_rectangle(x-w//2,y-h//2,x+w//2,y+h//2))
        self.transform(bodyPoint)
        draw_array(bodyPoint)

        rgb(255, 255, 255)
        borderPoint.extend(draw_rectangle(x-w//2,y-h//2,x+w//2,y+h//2))
        self.transform(borderPoint)
        draw_array(borderPoint)

        bodyPoint.clear()
        borderPoint.clear()

        rgb(223, 203, 126)
        bodyPoint.extend(fill_rectangle(x-w//6,y-h//6,x+w*4//5,y+h//6))
        self.transform(bodyPoint)
        draw_array(bodyPoint)

        borderPoint.extend(draw_rectangle(x-w//6,y-h//6,x+w*4//5,y+h//6))
        self.transform(borderPoint)
        draw_array(borderPoint)
    
    def block_coord(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        return (x//BLOCK_SIZE_W,y//BLOCK_SIZE_H)
    
    def ai(self,ob,pspeed = rotation_speed):
        mcord = self.block_coord()
        dcord = ob.block_coord()
        if self.target is None:
            paths = find_path_with_paths(node_paths,mcord,dcord)
            self.target = paths[1]
        
        tg = self.target

        dx = mcord[0] - tg[0]
        dy = mcord[1] - tg[1]
        np = mid_point(tg[0],tg[1])
        if np == (self.x, self.y):
            self.target = None
        dx = self.x - np[0]
        dy = self.y - np[1]
        
        ang = degrees(atan2(-dy,-dx))
        if ang < 0:
            ang += 360
        dist = sqrt((np[0]-self.x)**2+(np[1]-self.y)**2)

        speed = min(pspeed,dist)
        angDiff = min(pspeed,abs(ang-self.angle))
        
        if  angDiff == 0:
            self.move('w',speed)
        
        else:
            res = angDir(self.angle,ang)
            if res == 'cw':
                self.move('a',angDiff)
            else:
                self.move('d',angDiff)
            

    def destroy(self):
        entity.remove(self)

from collections import deque

def find_path_with_paths(paths, start, end):

  graph = {}
  for path in paths:
    p1, p2 = path
    if p1 not in graph:
      graph[p1] = set()
    if p2 not in graph:
      graph[p2] = set()
    graph[p1].add(p2)
    graph[p2].add(p1)

  visited = set()
  queue = deque([(start, [])])

  while queue:
    (current, path) = queue.popleft()

    if current == end:
      return path + [current]

    if current in visited:
      continue

    visited.add(current)

    for neighbor in graph.get(current, []):
      queue.append((neighbor, path + [current]))

  return None


userTank = Tank(BLOCK_SIZE_W//2,BLOCK_SIZE_H//2)

def keyboardListener(key, x, y):
    global ship_x
    if key == b'a':
        userTank.angle += rotation_speed
        if userTank.angle >= 360:
            userTank.angle = 0
   
    if key == b'd':
        userTank.angle -= rotation_speed
        if userTank.angle < 0:
            userTank.angle = 359
    if key == b'w':
        userTank.move('w')
    if key == b's':
        userTank.move('s')

    if key == b' ':
        userTank.fire()

def iterate():  
    glViewport(0, 0, SCREEN_W, SCREEN_H)  
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    glOrtho(0.0, BLOCK_SIZE_H*cells+1, 0.0, BLOCK_SIZE_H*cells+1, 0.0, 1.0)  
    glMatrixMode (GL_MODELVIEW)  
    glLoadIdentity()  
  
def showScreen():  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    glLoadIdentity()  
    iterate() 

    # Draw Map
    rgb(255,255,255)
    draw_array(map_state)

    # User Tank
    for ob in entity:
        ob.draw()

    for bullet in bullets:
        bullet.draw()
    

    glutSwapBuffers()  
    glutPostRedisplay()

def animate():
    for bullet in bullets[:]:
        state = bullet.move()
        collision = bullet.check_collision()
        if collision != bullet.owner and collision is not None:
            print(f"{collision.block_coord()} was hit by {bullet.owner.block_coord()}")
            bullet.destroy()
            collision.destroy()
            continue
        if state:
            bullet.destroy()
    for ob in entity[1:]:
        if randint(0,20) == 0:
            ob.fire()
        else:
            ob.ai(entity[0],rotation_speed/2)

initMap()

pos = [(cells-1,cells-1),(cells-1,0),(0,cells-1)]

for p in pos:
    np = mid_point(p[0],p[1])
    Tank(np[0],np[1])

glutInit()  
glutInitDisplayMode(GLUT_RGBA)  
glutInitWindowSize(SCREEN_W, SCREEN_H)  
glutInitWindowPosition(0, 0)  
wind = glutCreateWindow("Mank")  
glutDisplayFunc(showScreen)  
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMainLoop()  
#generateMage()
#print(ranDir())