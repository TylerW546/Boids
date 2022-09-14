import pygame
from pygame.locals import *

from main import *
from Environment import Environment
from PositionFormatter import PositionFormatter
from Functions import *

class Boid():
   objectSightRadius = 80
   sightRadius = 50

   ### SETTINGS FROM SETTINGS PANEL --------
   ## Toggling circles showing different radii, points, vectors, and lines
   # Shows how far the boid can see another boid
   entitySight = True
   # Shows how far the boid can see an object
   objectSight = True
   # Shows the average position of boids boid 0 can see.
   centerOfMass = True
   # Toggles vectors showing boid velocities.
   velocities = True
   # Highlights boids within boid 0's entity sight.
   neighbors = True
   # Highlights boid 0
   highlightMainBoid = True
   # Shows the user-drawn points of drawn lines.
   linePoints = True
   # Show the points that the program adds in between user-drawn points.
   subdivLinePoints = True
   # Highlights points within boid 0's object sight.
   seenPoints = True
    
   ### POINTS SETTINGS ---------------------
   ## Colors and Sizes of points
   mainPointColor = (150,150,0)
   mainPointSize = 3
   
   # The maximum length any wall segment can be without having a subdivided point.
   subdivLength = 50
   subdivideColor = (100,100,0)
   subdivideSize = 2
   
   pointHighlightColor = (255,255,0)
   pointHighlightSize = 4
   
   centerOfMassColor = (100,100,255)
   centerOfMassSize = 8
   
   ### BOID SETTINGS -----------------------
   ## Colors and sizes
   size = 3
   color = (255,255,255)
   neighborSize = 3
   mainSize = 5
   
   mainColor = (255,0,0)
   neighborsColor = (0,255,0)
   
   sightColor = (50,50,50)
   objectSightColor = (100,100,100)
   
   ## Maximum values for speed and force
   maxForce=.25
   maxSpeed=5
   maxObjectForce = 1

   ## Weights for the three different senses that boids act on.
   separationModifier = 1.5
   cohesionModifier = .5
   alignmentModifier = .6
   
   # The smaller this number is, the faster the boids will repel from objects. 
   # Avoiding objects must take priority over other factors as it is the most important or survival
   # This number is the factor that the other three senses are multiplied by.
   objectPriorityFactor = .2
   
   # Changes the length of velocity lines by the factor. Because boids move slowly, velocity lines are usually quite short.
   drawModifier = 2

   def __init__(self, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, velocity=[0,0], accel=[0,0]):
      self.x = x
      self.y = y
      
      self.velocity = velocity
      self.acceleration = accel
      
      self.targetVector = velocity
      
      self.nearby = []
      
   def update(self):
      # Get boids within range, fills self.nearby with their positions and velocities 
      self.getNears()
      
      # Move and draw based on velocity from previous frame
      self.move()
      self.draw()
      
      # 
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
      # Object Priority essentially shuts off all senses except object sense. If true, boid will prioritize moving away from walls.
      # This is set to false initially, but will be set to true if boid approaches any points
      self.objectPriority = False
      
      # Steer will be an average of vectors that will keep the boid away from points.
      steer = [0,0]
      # Keeps track of point count for averaging
      total = 0
      # Will be output
      avgVector = [0,0]
      
      ## Loops through all line in the Environment, and loops over all points in that line. This gets very slow with more lines, but works for a quick demonstration.
      for line in Environment.lines:
         # Subdivide. Boids could potentially slip through the lines if they have long stretches with no points.
         # Long stretches result from the user drawing lines too fast.
         points = subdivideLine(line[0:4], Boid.subdivLength)
         for point in points:
            dist = distance(point[0], point[1], self.x, self.y)
            
            ## If main boid, highlight the points (if booleans for highlighting points are True)
            if self == self.allBoids[0]:
               # Every line is defined as having main
               if point == points[0] or point == points[len(points)-1]:
                  # Boolean taken from settings
                  if Boid.linePoints:
                     pygame.draw.circle(screen, Boid.mainPointColor, (int(point[0]), int(point[1])), Boid.mainPointSize)
               else:
                  # Boolean taken from settings
                  if Boid.subdivLinePoints:
                     pygame.draw.circle(screen, Boid.subdivideColor, (int(point[0]), int(point[1])), Boid.subdivideSize)
               
               # Renders text of distance from boid 0 to every point.  
               #textsurface = myfont.render(str(round(dist)), False, (0, 0, 0))
               #screen.blit(textsurface,(int(point[0]), int(point[1])))
            
            # If the point is within this boid's sight
            if dist < Boid.objectSightRadius:
               # If screen should show seen points and this is the main boid, draw the seen points
               if Boid.seenPoints and self == PositionFormatter.boids[0]:
                  pygame.draw.circle(screen, Boid.pointHighlightColor, (int(point[0]), int(point[1])), Boid.pointHighlightSize)
               
               # Get unit vector of the difference between 
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
            
            # If there are points around, activate the object priority multiplier to basically ignore other boids and get away from the points ASAP
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
