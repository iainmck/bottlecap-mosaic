import math

def distance2d(p1, p2):
    (a1,a2) = p1
    (b1,b2) = p2
    return math.sqrt(math.pow(b1-a1,2) + math.pow(b2-a2,2))

def distance3d(p1, p2):
    (a1,a2,a3) = p1
    (b1,b2,b3) = p2
    return math.sqrt(math.pow(b1-a1,2) + math.pow(b2-a2,2) + math.pow(b3-a3,2))