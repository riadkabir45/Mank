from enum import Enum
Zone = Enum("Zone",[ (f"z{zone}",zone) for zone in range(9) ])

def draw_mpc(cx,cy,r):
    nPoint = []
    d = 1 - r
    x = r
    y = 0
    nPoint.extend(drawAllZone(x,y,cx,cy))
    while x >= y:
        if d > 0:
            d += 2*y - 2*x + 5
            x -= 1
            y += 1
        else:
            d += 2*y + 1
            y += 1
        nPoint.extend(drawAllZone(x,y,cx,cy))
    
    return nPoint


def drawAllZone(x,y,cx,cy):
    nPoint = []
    for rev in [True,False]:
        for my in [-1,1]:
            for mx in [-1,1]:
                point = list(coeffer(x,y,(mx,my,rev)))
                point[0] += cx
                point[1] += cy
                nPoint.append(point)
    return nPoint

def draw_mpl(x1,y1,x2,y2):
    nPoints = []
    
    size = 1
    zone = find_zone(x1,y1,x2,y2)
    if zone == Zone.z0:
        x1,y1,x2,y2 = coeffer2d(x1,y1,x2,y2,(1,1,False))
    elif zone == Zone.z1:
        x1,y1,x2,y2 = coeffer2d(x1,y1,x2,y2,(1,1,True))
    elif zone == Zone.z2:
        x1,y1,x2,y2 = coeffer2d(x1,y1,x2,y2,(1,-1,True))
    elif zone == Zone.z3:
        x1,y1,x2,y2 = coeffer2d(x1,y1,x2,y2,(-1,1,False))
    elif zone == Zone.z4:
        x1,y1,x2,y2 = coeffer2d(x1,y1,x2,y2,(-1,-1,False))
    elif zone == Zone.z5:
        x1,y1,x2,y2 = coeffer2d(x1,y1,x2,y2,(-1,-1,True))
    elif zone == Zone.z6:
        x1,y1,x2,y2 = coeffer2d(x1,y1,x2,y2,(-1,1,True))
    else:
        x1,y1,x2,y2 = coeffer2d(x1,y1,x2,y2,(1,-1,True))

    points = draw_mpl_z0(x1,y1,x2,y2)

    for point in points:
        if zone == Zone.z0:
            point = coeffer(point[0],point[1],(1,1,False))
            nPoints.append((point[0],point[1],size))
        elif zone == Zone.z1:
            point = coeffer(point[0],point[1],(1,1,True))
            nPoints.append((point[0],point[1],size))
        elif zone == Zone.z2:
            point = coeffer(point[0],point[1],(-1,1,True))
            nPoints.append((point[0],point[1],size))
        elif zone == Zone.z3:
            point = coeffer(point[0],point[1],(-1,1,False))
            nPoints.append((point[0],point[1],size))
        elif zone == Zone.z4:
            point = coeffer(point[0],point[1],(-1,-1,False))
            nPoints.append((point[0],point[1],size))
        elif zone == Zone.z5:
            point = coeffer(point[0],point[1],(-1,-1,True))
            nPoints.append((point[0],point[1],size))
        elif zone == Zone.z6:
            point = coeffer(point[0],point[1],(1,-1,True))
            nPoints.append((point[0],point[1],size))
        else:
            point = coeffer(point[0],point[1],(1,-1,False))
            nPoints.append((point[0],point[1],size))

    return nPoints

def coeffer2d(x1,y1,x2,y2,multiplier):
    x1, y1 = coeffer(x1,y1,multiplier)
    x2, y2 = coeffer(x2,y2,multiplier)
    return (x1,y1,x2,y2)

def coeffer(x1,y1,multiplier):
    mx, my, rev = multiplier
    if rev:
        x1,y1 = y1,x1
    return (mx*x1,my*y1)

def draw_mpl_z0(x1,y1,x2,y2):
    points = []

    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    dE = 2*dy
    dNE = 2*(dy - dx)
    x = x1
    y = y1

    points.append((x,y))
    while(x < x2):
        if d <= 0:
            x += 1
            d += dE
        else:
            x += 1
            y += 1
            d += dNE
        points.append((x,y))
    return points



def find_zone(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    adx = abs(dx)
    ady = abs(dy)
    if adx > ady:
        if dx < 0:
            if dy < 0:
                return Zone.z4
            return Zone.z3
        if dy < 0:
            return Zone.z7
        return Zone.z0
    else:
        if dx < 0:
            if dy < 0:
                return Zone.z5
            return Zone.z2
        if dy < 0:
            return Zone.z6
        return Zone.z1

