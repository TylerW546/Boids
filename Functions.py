import math

def distance(x1, y1, x2, y2):
   dist = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
   if dist == 0:
      return .001
   return dist

def vectorLen(vec):
   return distance(vec[0], vec[1], 0, 0)

def vecToLen(vector2, targetDistance):
   realDist = distance(0,0,vector2[0], vector2[1])
   fraction = targetDistance / realDist
   return([vector2[0] * fraction, vector2[1] * fraction])

def interceptPoint(lineCoord1, lineCoord2, point, angle):
   dx = lineCoord2[0] - lineCoord1[0]
   dy = lineCoord2[1] - lineCoord1[1]
   if dx == 0:
      return [point[0], dy]
   m1 = dy/dx
   b1 = lineCoord1[1] - m1 * lineCoord1[0]
   
   if m1 == 0:
      return [dx, point[1]]
   else:
      dx2 = math.cos(math.radians(angle))
      dy2 = math.sin(math.radians(angle))
      
      m2 = dy2/dx2
      b2 = point[1] - m2 * point[0]
      
      x = (b2-b1)/(m1-m2)
      y = m2*x+b2
   
   return [x,y]

def subdivideLine(line, segmentLength):
   points = []
   points.append(line[0:2])
   
   lineLen = distance(line[0], line[1], line[2], line[3])
   dx = line[2] - line[0]
   dy = line[3] - line[1]
   
   stepX = dx / lineLen * segmentLength
   stepY = dy / lineLen * segmentLength
   
   done = False
   stepNumber = 1
   while not done:
      if pointOnLine([line[0] + stepNumber * stepX, line[1] + stepNumber * stepY], line[0:2], line[2:4]):
         points.append([line[0] + stepNumber * stepX, line[1] + stepNumber * stepY])
      else:
         done = True
      stepNumber += 1
   
   points.append(line[2:4])
   return points

def pointOnLine(point, lineCoord1, lineCoord2):
   if point[0] <= max(lineCoord1[0], lineCoord2[0]) and point[0] >= min(lineCoord1[0], lineCoord2[0]):
      if point[1] <= max(lineCoord1[1], lineCoord2[1]) and point[1] >= min(lineCoord1[1], lineCoord2[1]):
         return True
   return False

def pointInCube(point, cubeCorner1, cubeCorner2):
   if point[0] <= max(cubeCorner1[0], cubeCorner2[0]) and point[0] >= min(cubeCorner1[0], cubeCorner2[0]):
      if point[1] <= max(cubeCorner1[1], cubeCorner2[1]) and point[1] >= min(cubeCorner1[1], cubeCorner2[1]):
         return True
   return False