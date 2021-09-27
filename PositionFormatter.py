from main import *

class PositionFormatter():
   boids = []
   boidPercent = .0001
   
   @staticmethod
   def startup():
      from Boid import Boid
      boidCount = int(SCREEN_WIDTH*SCREEN_HEIGHT*PositionFormatter.boidPercent)
      for i in range(boidCount):
         v = [0,0]
         v[0] = (random.randrange(100000)/100000-.5)*10
         v[1] = (random.randrange(100000)/100000-.5)*10
         a = [0,0]
         a[0] = (random.randrange(100000)/100000-.5)/2
         a[1] = (random.randrange(100000)/100000-.5)/2
         PositionFormatter.boids.append(Boid(x=random.randrange(0,SCREEN_WIDTH), y=random.randrange(0,SCREEN_HEIGHT), velocity=v, accel=a))
         
   @staticmethod
   def update():
      for boid in PositionFormatter.boids:
         boid.update()
   