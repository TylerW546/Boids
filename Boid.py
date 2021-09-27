import pygame
from pygame.locals import *

from main import *
from Environment import Environment
from PositionFormatter import PositionFormatter
from Functions import *

class Boid():
   objectSightRadius = 80
   sightRadius = 50

   # SETTINGS SETTINGS -------------------
   entitySight = True
   objectSight = True
   centerOfMass = True
   velocities = True
   neighbors = True
   highlightMainBoid = True
   linePoints = True
   subdivLinePoints = True
   seenPoints = True
    
   # POINTS SETTINGS ---------------------
   mainPointColor = (150,150,0)
   mainPointSize = 3
   
   subdivLength = 50
   subdivideColor = (100,100,0)
   subdivideSize = 2
   
   pointHighlightColor = (255,255,0)
   pointHighlightSize = 4
   
   centerOfMassColor = (100,100,255)
   centerOfMassSize = 8
   
   # BOID SETTINGS -----------------------
   size = 3
   color = (255,255,255)
   neighborSize = 3
   mainSize = 5
   
   mainColor = (255,0,0)
   neighborsColor = (0,255,0)
   
   sightColor = (50,50,50)
   objectSightColor = (100,100,100)
   
   
   maxForce=.25
   maxSpeed=5
   maxObjectForce = 2
   separationModifier = .5
   cohesionModifier = .5
   alignmentModifier = .5
   
   objectPriorityFactor = .005
   
   drawModifier = 2

   def __init__(self, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, velocity=[0,0], accel=[0,0]):
      self.x = x
      self.y = y
      
      self.velocity = velocity
      self.acceleration = accel
      
      self.targetVector = velocity
      
      self.nearby = []
      
   def update(self):
      self.getNears()
      
      self.move()
      self.draw()
      
      self.changeVectors = []
      
      separationLines = self.separationLines()
      self.acceleration[0] += separationLines[0]
      self.acceleration[1] += separationLines[1]
      
      interBoidalMultiplier = 1
      if self.objectPriority:
         interBoidalMultiplier = Boid.objectPriorityFactor
         
      separation = self.separation()
      self.acceleration[0] += separation[0] * interBoidalMultiplier * Boid.separationModifier
      self.acceleration[1] += separation[1] * interBoidalMultiplier * Boid.separationModifier
      
      align = self.alignment()
      self.acceleration[0] += align[0] * interBoidalMultiplier * Boid.alignmentModifier
      self.acceleration[1] += align[1] * interBoidalMultiplier * Boid.alignmentModifier
      
      cohesion = self.cohesion()
      self.acceleration[0] += cohesion[0] * interBoidalMultiplier * Boid.cohesionModifier
      self.acceleration[1] += cohesion[1] * interBoidalMultiplier * Boid.cohesionModifier
      
      #self.randomTurn()
      
      if Boid.velocities:
         self.drawVec()
   
   def getNears(self):
      # A list of boids in the format [x, y, angle]
      self.nearby = []
      from PositionFormatter import PositionFormatter
      self.allBoids = PositionFormatter.boids
      for boid in self.allBoids:
         if boid != self:
            if distance(boid.x, boid.y, self.x, self.y) < Boid.sightRadius:
               self.nearby.append([boid.x, boid.y, boid.velocity])
   
   def separationLines(self):
      self.objectPriority = False
      steer = [0,0]
      total = 0
      avgVector = [0,0]
      for line in Environment.lines:
         points = subdivideLine(line[0:4], Boid.subdivLength)
         for point in points:
            dist = distance(point[0], point[1], self.x, self.y)
            
            if self == self.allBoids[0]:
               if point == points[0] or point == points[len(points)-1]:
                  if Boid.linePoints:
                     pygame.draw.circle(screen, Boid.mainPointColor, (int(point[0]), int(point[1])), Boid.mainPointSize)
               else:
                  if Boid.subdivLinePoints:
                     pygame.draw.circle(screen, Boid.subdivideColor, (int(point[0]), int(point[1])), Boid.subdivideSize)
               
               #textsurface = myfont.render(str(dist), False, (0, 0, 0))
               #screen.blit(textsurface,(int(point[0]), int(point[1])))
            
            if dist < Boid.objectSightRadius:
               if Boid.seenPoints and self == PositionFormatter.boids[0]:
                  pygame.draw.circle(screen, Boid.pointHighlightColor, (int(point[0]), int(point[1])), Boid.pointHighlightSize)
               diff = [0,0]
               diff[0] = self.x - point[0]
               diff[1] = self.y - point[1]
               diff[0] /= dist
               diff[1] /= dist
               avgVector[0] += diff[0]
               avgVector[1] += diff[1]
               total += 1
         
         if total > 0:
            avgVector[0] /= total
            avgVector[1] /= total
            
            if vectorLen(avgVector) > 0:
               avgVector = vecToLen(avgVector, Boid.maxSpeed)
            
            steer[0] = avgVector[0] - self.velocity[0]
            steer[1] = avgVector[1] - self.velocity[1]
            
            if vectorLen(steer) > Boid.maxObjectForce:
               steer = vecToLen(steer, Boid.maxObjectForce)
            
            self.objectPriority = True
         
      return steer  
   
   def separation(self):
      steer = [0,0]
      total = len(self.nearby)
      avgVector = [0,0]
      for boid in self.nearby:
         dist = distance(boid[0], boid[1], self.x, self.y)
         diff = [0,0]
         diff[0] = self.x - boid[0]
         diff[1] = self.y - boid[1]
         
         diff[0] /= dist
         diff[1] /= dist
         avgVector[0] += diff[0]
         avgVector[1] += diff[1]
      
      if total > 0:
         avgVector[0] /= total
         avgVector[1] /= total
         
         if vectorLen(avgVector) > 0:
            avgVector = vecToLen(avgVector, Boid.maxSpeed)
         
         steer[0] = avgVector[0] - self.velocity[0]
         steer[1] = avgVector[1] - self.velocity[1]
         
         if vectorLen(steer) > Boid.maxForce:
            steer = vecToLen(steer, Boid.maxForce)
         
      return steer
   
   def alignment(self):
      steer = [0,0]
      total = len(self.nearby)
      avgVec = [self.velocity[0], self.velocity[1]]
      for boid in self.nearby:
         avgVec[0] += boid[2][0]
         avgVec[1] += boid[2][1]
      
      if total > 0:
         avgVec[0] /= total+1
         avgVec[1] /= total+1
         avgVec = vecToLen(avgVec, Boid.maxSpeed)
         steer[0] = avgVec[0] - self.velocity[0]
         steer[1] = avgVec[1] - self.velocity[1]
         
      return steer
   
   def cohesion(self):
      steer = [0, 0]
      total = len(self.nearby)
      centerOfMass = [self.x, self.y]
      for boid in self.nearby:
         centerOfMass[0] += boid[0]
         centerOfMass[1] += boid[1]
      
      if total > 0:
         centerOfMass[0] /= total+1
         centerOfMass[1] /= total+1

         if Boid.centerOfMass and self == PositionFormatter.boids[0]:
            pygame.draw.circle(screen, Boid.centerOfMassColor, (int(centerOfMass[0]), int(centerOfMass[1])), Boid.centerOfMassSize)

         centerOfMass[0] -= self.x
         centerOfMass[1] -= self.y
         
         if vectorLen(centerOfMass) > 0:
            centerOfMass = vecToLen(centerOfMass, Boid.maxSpeed)
         
         steer[0] = centerOfMass[0] - self.velocity[0]
         steer[1] = centerOfMass[1] - self.velocity[1]
         
         if vectorLen(steer) > Boid.maxForce:
            steer = vecToLen(steer, Boid.maxForce)
      
      return steer
   
   def randomTurn(self):
      if random.randrange(10) == 0:
         self.acceleration[0] += (random.randrange(100000)/100000-.5)/2
         self.acceleration[1] += (random.randrange(100000)/100000-.5)/2
   
   def move(self):
      self.x += self.velocity[0]
      self.y += self.velocity[1]
      self.velocity[0] += self.acceleration[0]
      self.velocity[1] += self.acceleration[1]
      
      if vectorLen(self.velocity) > Boid.maxSpeed:
         self.velocity = vecToLen(self.velocity, Boid.maxSpeed)
      
      self.acceleration = [0,0]
      
      if self.x < 0:
         self.x = SCREEN_WIDTH
      if self.y < 0:
         self.y = SCREEN_HEIGHT
         
      if self.x > SCREEN_WIDTH:
         self.x = 0
      if self.y > SCREEN_HEIGHT:
         self.y = 0
      
   def draw(self):
      from PositionFormatter import PositionFormatter
      if self == PositionFormatter.boids[0]:
         if Boid.objectSight or Boid.entitySight:
            if Boid.objectSightRadius >= Boid.sightRadius:
               if Boid.objectSight:
                  pygame.draw.circle(screen, Boid.objectSightColor, (int(self.x), int(self.y)), Boid.objectSightRadius)
               if Boid.entitySight:
                  pygame.draw.circle(screen, Boid.sightColor, (int(self.x), int(self.y)), Boid.sightRadius)
            else:
               if Boid.entitySight:
                  pygame.draw.circle(screen, Boid.sightColor, (int(self.x), int(self.y)), Boid.sightRadius)
               if Boid.objectSight:
                  pygame.draw.circle(screen, Boid.objectSightColor, (int(self.x), int(self.y)), Boid.objectSightRadius)
            
         if Boid.highlightMainBoid:
            pygame.draw.circle(screen, Boid.mainColor, (int(self.x), int(self.y)), Boid.mainSize)
         else:
            pygame.draw.circle(screen, Boid.color, (int(self.x), int(self.y)), Boid.size)
      elif Boid.neighbors and [PositionFormatter.boids[0].x, PositionFormatter.boids[0].y, PositionFormatter.boids[0].velocity] in self.nearby:
         pygame.draw.circle(screen, Boid.neighborsColor, (int(self.x), int(self.y)), Boid.neighborSize)
      else:
         pygame.draw.circle(screen, Boid.color, (int(self.x), int(self.y)), Boid.size)
      
   def drawVec(self):
      pygame.draw.lines(screen, Boid.color, True, [(int(self.x), int(self.y)), (int(self.x+self.velocity[0]*Boid.drawModifier), int(self.y+self.velocity[1]*Boid.drawModifier))], Boid.size)
