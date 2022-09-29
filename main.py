import math
import pygame
from pygame.locals import * # print
import random
import time

screen_width = 1080
screen_height = 600
fps = 60

screen = pygame.display.set_mode((screen_width, screen_height))
ability1overlay = pygame.Surface((56, 56))
ability2overlay = pygame.Surface((56, 56))
health = pygame.Surface((204, 24))
ability1overlay.set_alpha(100)
ability2overlay.set_alpha(100)
ability1overlay.set_colorkey((255,255,255))
ability2overlay.set_colorkey((255,255,255))
# Map info
MAP = [[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
      ,[2,0,0,0,0,0,0,0,0,0,0,0,0,0,2]
      ,[2,0,0,0,0,0,0,0,0,0,2,2,2,0,2]
      ,[2,0,0,0,2,2,0,0,0,0,2,2,2,0,2]
      ,[2,0,0,0,2,2,0,0,0,0,0,0,0,0,2]
      ,[2,0,0,0,2,2,0,0,0,0,0,0,0,0,2]
      ,[2,0,0,0,0,0,0,0,0,0,0,0,0,0,2]
      ,[2,0,0,0,0,0,0,0,0,0,0,0,0,0,2]
      ,[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]

 
def update_rainbow(rainbow, rainbow_pos):
   """ Updates rainbow and brings it through the different fades between Red, Green, and Blue """
   rainbow[rainbow_pos] -= 10
   rainbow[rainbow_pos-1] += 10
   if rainbow[rainbow_pos] < 0:
      rainbow[rainbow_pos] = 0
      rainbow[rainbow_pos-1] = 255
      rainbow_pos -= 1
   if rainbow_pos < 0:
      rainbow_pos = 2
   return rainbow, rainbow_pos
# Sorts through given
def sort(list):
   output = []
   index = 0
   while len(list):
      smallest = list[0]
      for k in range(len(list)):
         if list[k] <= smallest:
            smallest = list[k]
            index = k
      del list[index]
      output.append(smallest)
   return output    
# Hit Box
def check_border(x, y, HB, BLOCK_SIZE):
   """ Checks if corner clips into wall during movement """
   if MAP[round((y-HB-11)//BLOCK_SIZE)][round((x-HB-10)//BLOCK_SIZE)]:
      return False
   if MAP[round((y-HB-11)//BLOCK_SIZE)][round((x+HB+10)//BLOCK_SIZE)]:
      return False
   if MAP[round((y+HB+11)//BLOCK_SIZE)][round((x+HB+10)//BLOCK_SIZE)]:
      return False
   if MAP[round((y+HB+11)//BLOCK_SIZE)][round((x-HB-10)//BLOCK_SIZE)]:
      return False
   return True
# Sorts through given
def sort(list):
   output = []
   index = 0
   while len(list):
      smallest = list[0]
      for k in range(len(list)):
         if list[k] <= smallest:
            smallest = list[k]
            index = k
      del list[index]
      output.append(smallest)
   return output  
 
 
# Distance finder to given points
def distance(pos_1, pos_2):
   """ Finds distance between two points """
   return abs(math.sqrt(((pos_1[0]-pos_2[0])**2)+((pos_1[1]-pos_2[1])**2)))
def ray(angle, x, y, angle_offset, BLOCK_SIZE):
  """ Finds given distance of a ray before hitting a wall"""
  if angle >= 360:
    angle -= 360
    angle = round(angle, 10)
  point_x = 0 # End point of ray on x-axis
  point_y = 0 # End point of ray on y-axis
  square_y = int(y//BLOCK_SIZE) # Current block position
  square_x = int(x//BLOCK_SIZE)
  # If angle is multiple of 90 to prevent going through trig functions
  if angle % 90 == 0:
    # Increase square_x until reached wall
    if angle == 0:
      point_y = y
      while  not MAP[square_y][square_x]:
        square_x += 1
      point_x = square_x * BLOCK_SIZE
      return distance((x, y), (point_x, point_y)), MAP[square_y][square_x]
    elif angle == 180:
      # Decreases square_x until reached wall
      point_y = y
      while  not MAP[square_y][square_x]:
        square_x -= 1
      point_x = (square_x+1) * BLOCK_SIZE
      return distance((x, y), (point_x, point_y)), MAP[square_y][square_x]
    elif angle == 270:
      # Decreases square_y until reached wall
      point_x = x
      while not MAP[square_y][square_x]:
        square_y -= 1
      point_y = (square_y+1) * BLOCK_SIZE
      return distance((x, y), (point_x, point_y)), MAP[square_y][square_x]
    elif angle == 90:
      # Increase square_y until reached wall
      point_x = x
      while not MAP[square_y][square_x]:
        square_y += 1
      point_y = square_y * BLOCK_SIZE
      return distance((x, y), (point_x, point_y)), MAP[square_y][square_x]
 
  else: # If angle not multiple of 90
    x_off = (1/math.tan(math.radians(angle)))*BLOCK_SIZE  # Initial y offset for reaching nearest grid edge on y-axis
    y_off = (-(math.tan(math.radians(angle))))*BLOCK_SIZE # Initial x offset for reaching nearest grid edge on x-axis
    if angle > 180: # Separate into two groups for whether y_1 is closest to y-axis above or below
      y_1 = y%BLOCK_SIZE # Distance between y and closest y-axis above it
      first_y = (-y_1)/math.tan(math.radians(angle))# X offset for reaching y
 
      if angle < 270: # Separate in two groups for whether x_1 is closest y-axis above or below
        x_1 = x%BLOCK_SIZE # Distance between x and closest x-axis to the right of it
        first_x = (-x_1)*math.tan(math.radians(angle)) # Y offset for reach x
        point_1 = ((x+first_y), (y-y_1)) # Point for next x intercept
        point_2 = ((x-x_1), (y+first_x)) # Point for next y intercept
   
        # Moves points across x and y intercepts until reach wall, while updating end of ray point
        while not MAP[square_y][square_x]:
           if distance(point_1, (x, y)) <= distance(point_2, (x, y)):
             square_y -= 1
             point_x = point_1[0]
             point_y = point_1[1]
             point_1 = (point_1[0]-x_off, point_1[1]-BLOCK_SIZE)
           else:
             square_x -= 1
             point_x = point_2[0]
             point_y = point_2[1]
             point_2 = (point_2[0]-BLOCK_SIZE, point_2[1]+y_off)
      else:
        x_1 = BLOCK_SIZE-(x%BLOCK_SIZE) # Distance between x and closest x-axis to the left of it
        first_x = (-x_1)*math.tan(math.radians(angle)) # Y offset for reach x
        point_1 = ((x+first_y), (y-y_1)) # Point for next x-interceptor
        point_2 = ((x+x_1), (y-first_x)) # Point for next y-interceptor
        while not MAP[square_y][square_x]: # Moves points across x and y interspets until reach wall, while updating end of ray point
          if distance(point_1, (x, y)) <= distance(point_2, (x, y)): # Compares distances for next two points and selects closest
            square_y -= 1
            point_x = point_1[0]
            point_y = point_1[1]
            point_1 = (point_1[0]-x_off, point_1[1]-BLOCK_SIZE)
          else:
            square_x += 1
            point_x = point_2[0]
            point_y = point_2[1]
            point_2 = (point_2[0]+BLOCK_SIZE, point_2[1]-y_off)
         
    else: # Distance between y and closest y-axis below it
        y_1 = BLOCK_SIZE-(y%BLOCK_SIZE) # Distance between y and closest y-axis below it
        first_y = (-y_1)/math.tan(math.radians(angle))# X offset for reach y
        if angle > 90: # Separate in two groups for whether x_1 is closest y-axis above or below
            x_1 = x%BLOCK_SIZE # Distance between x and closest x-axis to the right of it
            first_x = (-x_1)*math.tan(math.radians(angle))# Y offset for reach x
            point_1 = (x-first_y, y+y_1) # Point for next x-intercept
            point_2 = (x-x_1, y+first_x) # Point for next x-intercept
            while not MAP[square_y][square_x]: # Moves points across x and y intercepts until reach wall, while updating end of ray point
                if distance(point_1, (x, y)) < distance(point_2, (x, y)): # Compares distances for next two points and selects closest
                    square_y += 1
                    point_x = point_1[0]
                    point_y = point_1[1]
                    point_1 = (point_1[0]+x_off, point_1[1]+BLOCK_SIZE)
                else:
                    square_x -= 1
                    point_x = point_2[0]
                    point_y = point_2[1]
                    point_2 = (point_2[0]-BLOCK_SIZE, point_2[1]+y_off)
        else:
            x_1 = BLOCK_SIZE-(x%BLOCK_SIZE) # Distance between x and closest x-axis to the left of it
            first_x = (-x_1)*math.tan(math.radians(angle))# Y offset for reach x
            point_1 = ((x-first_y), (y+y_1)) # Point for next x-intercept
            point_2 = ((x+x_1), (y-first_x)) # Point for next x-intercept
            while not MAP[square_y][square_x]: # Moves points across x and y intercepts until reach wall, while updating end of ray point
                if distance(point_1, (x, y)) < distance(point_2, (x, y)): # Compares distances for next two points and selects closest
                    square_y += 1
                    point_x = point_1[0]
                    point_y = point_1[1]
                    point_1 = (point_1[0]+x_off, point_1[1]+BLOCK_SIZE)
                else:
                    square_x += 1
                    point_x = point_2[0]
                    point_y = point_2[1]
                    point_2 = (point_2[0]+BLOCK_SIZE, point_2[1]-y_off)
    color = MAP[square_y][square_x]
    return distance((x, y), (round(point_x), round(point_y)))*math.cos(math.radians(angle_offset)), color # Return ray distance and wall number for its color

 
def entity_calcs(xpos,ypos, playerang, playerx, playery):      
   """ Calculates visibility, angle offset in FOV and distance """
   xoff = playerx-xpos
   yoff = playery-ypos
   if not xoff:
      xoff += 0.001
   if not yoff:
      yoff += 0.001
   # Getting entity angle
   entity_angle = math.degrees(math.atan(xoff/yoff)) # Relative angle from player
   # Quads 1 and 2:
   if xoff > 0:
      # 1
      if yoff > 0:
         entity_angle = 270 - entity_angle
      # 2
      else:
         entity_angle = 90 - entity_angle
   # Quads 3 and 4:
   else:
      # 4
      if yoff > 0:
         entity_angle = 270 - entity_angle
      # 3
      else:
         entity_angle = 90 - entity_angle
   visible = False
   angle_offset = 0
   # Checking if on screen
   if  -5 <= entity_angle - playerang <= Player.FOV + 5:
      visible = True
      angle_offset = entity_angle - playerang
   if not visible:
      if playerang + Player.FOV > 360:
         playerang = (playerang + Player.FOV) % 360
         if entity_angle <= playerang+5:
            visible = True
            angle_offset = Player.FOV - (playerang - entity_angle)
   # Finding Distance
   distance = math.sqrt((playerx - xpos) ** 2 + (playery - ypos) ** 2) * math.cos(math.radians(abs(angle_offset-30)))
   if distance < 30:
      distance = 30
      visible = False
   return visible, angle_offset, distance
 
class Sprite():
   sprites = []
   
   def __init__(self, image=None, x=0, y=0, right=None, bottom=None):
      self.image = image
      
      self.x = x
      self.y = y
      
      if right:
         self.x = right-image.get_width()
      if bottom:
         self.y = bottom-image.get_height()
      
      Sprite.sprites.append(self)
   
   def destroy(self):
      Sprite.sprites.remove(self)
   
   def update(self):
      pass
   
   @staticmethod  
   def update_all():
      for sprite in Sprite.sprites:
         sprite.update()
   

 
class Shot(Sprite):
   image = pygame.image.load("shot.png")
   image.set_colorkey((255,255,255))
   Hproportion = 5000 # Proportion for height of shot
   Wproportion = Hproportion # Proportion of width of shot
   imagesize = 56
   def __init__(self, x, y, dx, dy):
      super(Shot, self).__init__(image = Shot.image, x = -100, y = 0)
      self.xpos = x
      self.ypos = y
      self.dx = dx
      self.dy = dy
      self.visible = False
      self.distance = 0
   def get_updated(self, playerx, playery, playerang):
      # Getting x and y offsets, then preventing them from being 0
      self.xpos += self.dx
      self.ypos += self.dy  
      self.visible, self.angle_offset, self.distance = entity_calcs(self.xpos, self.ypos, playerang, playerx, playery)
      self.find_render()
      self.check_wall_collision()
      self.check_entity_collision()
 
   def find_render(self):
      # if visible find its position on screen, width, and height
      if self.visible:
         self.renderx = (self.angle_offset/Player.FOV) * 1080 # x position on screen
         self.rendery = screen_height // 2
         self.myheight = int(Shot.Hproportion//self.distance)
         self.mywidth = int(Shot.Wproportion//self.distance)
         self.image = pygame.transform.scale(Shot.image, (self.mywidth, self.myheight)) # height of alien on screen
   def check_entity_collision(self):
      for entity in Game.entities:
         try:
            entity.aliencheck()
            if self.xpos <= entity.xpos + entity.HB * 3 and self.xpos >= entity.xpos - entity.HB * 3 and self.ypos >= entity.ypos - entity.HB * 3 and self.ypos <= entity.ypos + entity.HB * 3:
               entity.destroy()
               Game.entities.remove(entity)
               self.destroy()
               Game.entities.remove(self)
               Game.kills += 1
         except:
            pass
   def check_wall_collision(self):
      if MAP[int(self.ypos//200)][int(self.xpos//200)]:
         self.destroy()
         Game.entities.remove(self)
   def draw(self):
      if self.visible:
         screen.blit(self.image, (self.renderx - self.mywidth // 2, self.rendery - self.myheight // 2))



class Alien(Sprite):
   image = pygame.image.load("Alien.png").convert_alpha()
   image.set_colorkey((255,0,0))
   Hproportion = 180000 # Proportion for height of alien
   Wproportion = Hproportion * 5/9 # Proportion of width of alien
   speed = 5
   def __init__(self, movements):
      super(Alien, self).__init__(image = Alien.image, x = -100, y = 0)
      if movements == "pathfind":
         self.xpos = 1500
         self.ypos = 900
      else:
         self.xpos = movements[0][0]
         self.ypos = movements[0][1]

      self.dx = 0
      self.dy = 0
      self.visible = False
      self.movements = movements
      self.HB = 20
      self.moveindex = 0
      self.maxhitcool = 50
      self.hitcooldown = self.maxhitcool
 
   def get_updated(self, playerx, playery, playerang):
      # Getting x and y offsets, then preventing them from being 0
      self.visible, self.angle_offset, self.distance = entity_calcs(self.xpos, self.ypos, playerang, playerx, playery)
     
      for play in Sprite.sprites:
            try:
               play.playercheck
               player = play
            except:
               pass
     
      self.find_render()
      self.attack(player)
      self.move(player)
   
      if self.hitcooldown:
         self.hitcooldown -= 1
 
   def attack(self, player):
      if not self.hitcooldown:
         if player.xpos > self.xpos - self.HB and player.xpos < self.xpos + self.HB and player.ypos > self.ypos - self.HB and player.ypos < self.ypos + self.HB:
            player.health -= 1
            self.hitcooldown = self.maxhitcool
   
     
   
   def find_render(self):
      # if visible find its position on screen, width, and height
      if self.visible:
         self.renderx = (self.angle_offset/Player.FOV) * 1080 # x position on screen
         self.rendery = screen_height // 2
         self.myheight = int(Alien.Hproportion//self.distance)
         self.mywidth = int(Alien.Wproportion//self.distance)
     
         self.image = pygame.transform.scale(Alien.image, (self.mywidth, self.myheight)) # height of alien on screen
         self.image.set_colorkey((255,0,0))

 
   def move(self, player):
      if check_border(self.xpos + self.dx, self.ypos + self.dy, self.HB, Draw.BLOCK_SIZE):
         self.xpos += self.dx
         self.ypos += self.dy
   
      if self.movements == "pathfind":
         self.dest = (player.xpos,player.ypos)
      else:
         self.dest = self.movements[self.moveindex]
      # If at move's point
      if round(self.xpos) == self.dest[0] and round(self.ypos) == self.dest[1]:
         # Next move:
         self.xpos = self.dest[0]
         self.ypos = self.dest[1]
         self.dx = 0
         self.dy = 0
       
         self.moveindex += 1
         if self.moveindex > len(self.movements) - 1:
            self.moveindex = 0
   
      # Going to move's point
      else:
         self.xfromdest = self.dest[0] - self.xpos
         self.yfromdest = self.dest[1] - self.ypos
       
         self.disttopoint = math.sqrt(self.xfromdest ** 2 + self.yfromdest ** 2)
         self.num_steps_to_dest = self.disttopoint / Alien.speed
       
         if self.num_steps_to_dest != 0:
            self.dx = self.xfromdest / self.num_steps_to_dest
            self.dy = self.yfromdest / self.num_steps_to_dest
         else:
            self.dx = 0
            self.dy = 0
       
         if self.disttopoint < Alien.speed * 1.5:
            self.xpos = self.dest[0]
            self.ypos = self.dest[1]
            self.dx = 0
            self.dy = 0
 
   def draw(self):
      if self.visible:
         screen.blit(self.image, (self.renderx - self.mywidth // 2, self.rendery - self.myheight // 2))
 
   def aliencheck(self):
      pass

class Smoker(Sprite):
   image = pygame.image.load("SmokerEnt.png")
   image.set_colorkey((127,127,127))
   Hproportion = 20000 # Proportion for height
   Wproportion = Hproportion * 5/9 # Proportion of width to height
   Height_proportion = 75000 # for smokers z value relative to wall, value is equal to half the wall proporiton
   imagesize = 56
 
   def __init__(self, x, y, dx, dy):
      super(Smoker, self).__init__(image = Smoker.image, right = -1, bottom = -1)
      self.xpos = x
      self.ypos = y
      self.zpos = 0 # height of smoker
     
      self.dx = dx
      self.dy = dy
      self.dz = -5 # starting velocity on z axis
      self.visible = False
      self.visable = False
     
      self.exploding = False
      self.explodetime = 0
     
      self.fuse = random.randrange(140, 160)
     
      self.smokingtime = random.randrange(200, 250)
 
   def get_updated(self, playerx, playery, playerang):
      # Getting x and y offsets, then preventing them from being 0
      self.xpos += self.dx
      self.ypos += self.dy  
      self.visible, self.angle_offset, self.distance = entity_calcs(self.xpos, self.ypos, playerang, playerx, playery)
     
      self.fuse -= 1
      if self.fuse < 0:
         self.exploding = True
     
      self.update_fall()
      self.find_render()
      self.wallbounce()
      self.explode()
   
   def update_fall(self):
      self.zpos -= self.dz
      self.dz += 0.3
      if self.zpos < -100:
         # self.dz = -self.dz * 0.6
         self.dz = -self.dz * (random.randrange(500, 1000)/1000)
         self.dx *= 0.8
         self.dy *= 0.8
         self.zpos = -99.99
      if self.zpos > 100:
         self.dz = -self.dz * 0.6
         self.dx *= 0.8
         self.dy *= 0.8
         self.zpos = 99.99    
   def explode(self): # if explodes remove smoker object and add explosion
      if self.exploding:
         if self.explodetime % 2 == 0:
            Game.entities.append(Smoke(random.randrange(30000, 34000), 100, self.xpos, self.ypos, self.zpos, 5, 5))
         else:
            Game.entities.append(Smoke(random.randrange(39000, 47000), 100, self.xpos, self.ypos, self.zpos, 5, 3))  
         self.explodetime += 1
      if self.explodetime > self.smokingtime:
         self.destroy()
         Game.entities.remove(self)
   def find_render(self):
      # if visible find its position on screen, width, and height
      if self.visible:
         self.renderx = (self.angle_offset/Player.FOV) * 1080 # x position on screen
         self.rendery = screen_height // 2 - (((self.Height_proportion/self.distance)/100)*self.zpos)
         self.myheight = int(Smoker.Hproportion//self.distance)
         self.mywidth = int(Smoker.Wproportion//self.distance)
         self.image = pygame.transform.scale(Smoker.image, (self.mywidth, self.myheight)) # Scale of  on screen
   def draw(self):
      if self.visible:
         screen.blit(self.image, (self.renderx - self.mywidth // 2, self.rendery - self.myheight // 2))
   def wallbounce(self):
      if MAP[int((self.ypos + 2 * self.dy)//200)][int((self.xpos)//200)]:
         self.dy = -self.dy
         self.xpos += self.dx
      if MAP[int((self.ypos)//200)][int((self.xpos + 2 * self.dx)//200)]:
         self.dx = -self.dx
         self.ypos += self.dy

class Grenade(Sprite):
   image = pygame.image.load("GrenEnt.png")
   image.set_colorkey((255,255,255))
   Hproportion = 20000 # Proportion for heigh
   Wproportion = Hproportion * 5/9 # Proportion of width to height
   Height_proportion = 75000 # for grendades z value relative to wall, value is equal to half the wall proporiton
   imagesize = 56
   def __init__(self, x, y, dx, dy):
      super(Grenade, self).__init__(image = Grenade.image, right = -1, bottom = -1)
      self.xpos = x
      self.ypos = y
      self.zpos = 0 # height of grenade
     
      self.dx = dx
      self.dy = dy
      self.dz = -5 # starting velocity on z axis
      self.visible = False
      self.visable = False
     
      self.fuse = random.randrange(140, 160)
 
   def get_updated(self, playerx, playery, playerang):
      # Getting x and y offsets, then preventing them from being 0
      self.xpos += self.dx
      self.ypos += self.dy  
      self.visible, self.angle_offset, self.distance = entity_calcs(self.xpos, self.ypos, playerang, playerx, playery)
     
      self.fuse -= 1
      if self.fuse < 0:
         self.explode()
     
      self.update_fall()
      self.find_render()
      self.wallbounce()
   
   def update_fall(self):
      self.zpos -= self.dz
      self.dz += 0.1
      if self.zpos < -100:
         # self.dz = -self.dz * 0.6
         self.dz = -self.dz * (random.randrange(500, 1000)/1000)
         self.dx *= 0.8
         self.dy *= 0.8
         self.zpos = -99.99
      if self.zpos > 100:
         self.dz = -self.dz * 0.6
         self.dx *= 0.8
         self.dy *= 0.8
         self.zpos = 99.99
   def explode(self): # if explodes remove grenade object and add explosion
      self.destroy()
      Game.entities.remove(self)
      Game.entities.append(Explosion(150000, 50, self.xpos, self.ypos, self.zpos))
   def find_render(self):
      # if visible find its position on screen, width, and height
      if self.visible:
         self.renderx = (self.angle_offset/Player.FOV) * 1080 # x position on screen
         self.rendery = screen_height // 2 - (((self.Height_proportion/self.distance)/100)*self.zpos)
         self.myheight = int(Grenade.Hproportion//self.distance)
         self.mywidth = int(Grenade.Wproportion//self.distance)
         self.image = pygame.transform.scale(Grenade.image, (self.mywidth, self.myheight)) # Scale of  on screen
   def draw(self):
      if self.visible:
         screen.blit(self.image, (self.renderx - self.mywidth // 2, self.rendery - self.myheight // 2))
   def wallbounce(self):
      if MAP[int((self.ypos + 2 * self.dy)//200)][int((self.xpos)//200)]:
         self.dy = -self.dy
         self.xpos += self.dx
      if MAP[int((self.ypos)//200)][int((self.xpos + 2 * self.dx)//200)]:
         self.dx = -self.dx
         self.ypos += self.dy

class Smoke(Sprite):
   image = pygame.image.load("smoke.png")
   image.set_colorkey((255,255,255))
   Height_proportion = 75000 # proportion of ofset y value for explosions z value
 
   def __init__(self, size, life, x, y, z, up, spread):# Size of explosition and how long it lasts
     super(Smoke, self).__init__(image = Smoke.image, right = -1, bottom = -1)
     self.xpos = x
     self.ypos = y
     self.zpos = z
     self.proportion = size
     self.spread_radius = spread
     self.dz = up
   
     self.life_time = life
     self.visible = False
   
     self.dx = random.randrange(-self.spread_radius, self.spread_radius)
     self.dy = random.randrange(-self.spread_radius, self.spread_radius)
   
   def get_updated(self, playerx, playery, playerang):
      if check_border(self.xpos + self.dx, self.ypos, 1, Draw.BLOCK_SIZE):
         self.xpos += self.dx
      if check_border(self.xpos, self.ypos + self.dy, 1, Draw.BLOCK_SIZE):
         self.ypos += self.dy
      self.zpos += self.dz
     
      if self.zpos > 100:
         self.zpos = 100
     
      self.visible, self.angle_offset, self.distance = entity_calcs(self.xpos, self.ypos, playerang, playerx, playery)
     
      self.find_render()
     
      self.life_time -= 1
      if self.life_time < 0:
         Game.entities.remove(self)
         self.destroy()
   
   def find_render(self):
      # if visible find its position on screen, width, and height
      if self.visible:
         self.renderx = (self.angle_offset/Player.FOV) * 1080 # x position on screen
         self.rendery = screen_height // 2 - (((self.Height_proportion/self.distance)/100)*self.zpos)
         self.myheight = int(self.proportion//self.distance)
         self.mywidth = self.myheight
     
         self.image = pygame.transform.scale(Smoke.image, (self.mywidth, self.myheight)) # Scale of  on screen
   def draw(self):
      if self.visible:
         screen.blit(self.image, (self.renderx - self.mywidth // 2, self.rendery - self.myheight // 2))
     

class Explosion(Sprite):
   image = pygame.image.load("explosion.png")
   image.set_colorkey((255,255,255))
   Height_proportion = 75000 # proportion of ofset y value for explosions z value
 
   def __init__(self, size, life, x, y, z):# Size of explosition and how long it lasts
     super(Explosion, self).__init__(image = Grenade.image, right = -1, bottom = -1)
   
     self.xpos = x
     self.ypos = y
     self.zpos = z
     self.proportion = size
     self.explosion_size = size/750
     self.max_life = life
     self.life_time = self.max_life
     self.visible = False
     self.check_entity_damage()
   
     self.percentsize = 0
   def get_updated(self, playerx, playery, playerang):
     
      self.percentsize += 2 / self.max_life
     
      self.visible, self.angle_offset, self.distance = entity_calcs(self.xpos, self.ypos, playerang, playerx, playery)
     
      self.find_render()
     
      self.check_entity_damage()
      self.life_time -= 1
      if self.life_time < 0:
         Game.entities.remove(self)
         self.destroy()
   def check_entity_damage(self):
      for entity in Game.entities:
         try:
            entity.check()
            if self.xpos <= entity.xpos + self.explosion_size and self.xpos >= entity.xpos - self.explosion_size and self.ypos >= entity.ypos - self.explosion_size and self.ypos <= entity.ypos + self.explosion_size:
               entity.destroy()
               Game.entities.remove(entity)
               Game.kills += 1
         except:
            pass
   def find_render(self):
      # if visible find its position on screen, width, and height
      if self.visible:
         self.renderx = (self.angle_offset/Player.FOV) * 1080 # x position on screen
         self.rendery = screen_height // 2 - (((self.Height_proportion/self.distance)/100)*self.zpos)
         self.myheight = int(self.proportion//self.distance * self.percentsize)
         self.mywidth = self.myheight
     
         self.image = pygame.transform.scale(Explosion.image, (self.mywidth, self.myheight)) # Scale of  on screen
   def draw(self):
      if self.visible:
         screen.blit(self.image, (self.renderx - self.mywidth // 2, self.rendery - self.myheight // 2))
     
class Game():
   bulletspeed = 50
   grenspeed = 20
   smokerspeed = 20
 
   vanishlen = 36000
 
   kills = 0
 
   entities = [Alien(((700,500), (1300,500),(1300,1300), (700, 1300))), Alien(((1900, 300),(2700, 300),(2700, 900),(1900, 900))), Alien("pathfind")] # Enemies and other things
 
class Inputs():
   keys = []
   mouse_buttons = []
   mouse_position = []
   
   @staticmethod
   def update():
      Inputs.keys = pygame.key.get_pressed()
      Inputs.mouse_buttons = pygame.mouse.get_pressed()
      Inputs.mouse_position = pygame.mouse.get_pos()
 

class Player(Sprite):
   """ Player. Movement and GUI """
   handimage = pygame.image.load("gunhand.png")
   handimage.set_colorkey((255,255,255))
   FOV = 60 # Angle for the cast of rays
 
   def __init__(self):
      super(Player, self).__init__(image = Player.handimage, right = screen_width - 50, bottom = screen_height + 10)
 
      self.lastmouseposition = (screen_width // 2, screen_height // 2)
 
      self.BLOCK_SIZE = 200
 
      self.xpos = self.BLOCK_SIZE*1.5 # Player starts in top left
      self.ypos = self.BLOCK_SIZE*1.5 # Player starts in top right
      self.x_1 = self.xpos # Temp x and y to check if a move is possible or collides with a wall
      self.y_1 = self.ypos
      self.ang = 0 # Starting angle of left side of screen
 
      self.walk = 15 # Steps taken for each frame
      self.sprint = self.walk * 2 # Faster movement
      self.HB = 20 # Hit box or radius of character
 
      self.move = False
 
      self.ability1cooldown = 0
      self.ability1maxcool = 20
      self.ability2cooldown = 0
      self.ability2maxcool = 20
 
      self.maxhealth = 10
      self.health = self.maxhealth
 
      self.maxammo = 10
      self.ammo = self.maxammo
   
      self.shotcool = 0
      self.shotmaxcool = 0
      self.healthSurf = pygame.Surface((204, 24))
 
   def update(self):
      self.inputs()
 
      self.movement()
      self.turn()
 
      self.cooldowns()
 
      self.draw_health()
 
      if self.health < 1:
         self.die()
      screen.blit(Player.handimage, (self.x, self.y))
 
   def inputs(self):
      if Inputs.keys[pygame.K_e]:
         if not self.ability1cooldown:
            self.ability1cooldown = self.ability1maxcool
            self.throwGren()
      if Inputs.keys[pygame.K_r]:
         if not self.ability2cooldown:
            self.ability2cooldown = self.ability1maxcool
            self.throwSmoke()
      if Inputs.mouse_buttons[0]:
         if not self.shotcool:
            self.shotcool = self.shotmaxcool
            self.shoot()
   
      # For health testing
      # if Inputs.keys[pygame.K_SPACE]:
      #    self.health -= 1
   
 
   def cooldowns(self):
      if self.ability1cooldown > 0:
         self.ability1cooldown -= 1
      if self.ability2cooldown > 0:
         self.ability2cooldown -= 1
      if self.shotcool > 0:
         self.shotcool -= 1
       
   def draw_health(self):
      self.healthpix = round(self.health / self.maxhealth * 200)
      self.healthSurf.fill((0,0,0))
      if self.health > 0:
         pygame.draw.rect(self.healthSurf, (255,0,0), (2, 2, self.healthpix, 20), 0)
      screen.blit(self.healthSurf, (screen_width//2 - 102, screen_height - 40))
 
   def movement(self):
        self.x_1 = self.xpos
        self.y_1 = self.ypos
        if Inputs.keys[pygame.K_w]: # Going forward
           if Inputs.keys[pygame.K_LSHIFT]: # If sprinting
              self.x_1 += self.sprint * math.cos(math.radians(int((self.ang+(Player.FOV/2))%360)))
              self.y_1 += self.sprint * math.sin(math.radians(int((self.ang+(Player.FOV/2))%360)))
           else:                  # If walking
              self.x_1 += self.walk * math.cos(math.radians(int((self.ang+(Player.FOV/2))%360)))
              self.y_1 += self.walk * math.sin(math.radians(int((self.ang+(Player.FOV/2))%360)))
           self.move = True
        if Inputs.keys[pygame.K_a]: # To the left
           self.x_1 += self.walk * math.cos(math.radians(int((self.ang+(Player.FOV/2)-90)%360)))
           self.y_1 += self.walk * math.sin(math.radians(int((self.ang+(Player.FOV/2)-90)%360)))
           self.move = True
        if Inputs.keys[pygame.K_d]: # To the right
           self.x_1 += self.walk * math.cos(math.radians(int((self.ang+(Player.FOV/2)+90)%360)))
           self.y_1 += self.walk * math.sin(math.radians(int((self.ang+(Player.FOV/2)+90)%360)))
           self.move = True
        if Inputs.keys[pygame.K_s]: # Backwards
           self.x_1 += self.walk * math.cos(math.radians(int((self.ang+(Player.FOV/2)+180)%360)))
           self.y_1 += self.walk * math.sin(math.radians(int((self.ang+(Player.FOV/2)+180)%360)))
           self.move = True
   
        if self.move: # Check if x and y after movement don't clip into wall
           if check_border(self.x_1, self.ypos, self.HB, self.BLOCK_SIZE):
              self.xpos = self.x_1
           if check_border(self.xpos, self.y_1, self.HB, self.BLOCK_SIZE):
              self.ypos = self.y_1
           self.move = False
 
   def turn(self):
      self.ang -= (self.lastmouseposition[0] - Inputs.mouse_position[0]) / 10
      if Inputs.mouse_position[0] > screen_width - 100 or Inputs.mouse_position[0] < 100:
         pygame.mouse.set_pos((screen_width // 2, screen_height // 2))
         self.lastmouseposition = pygame.mouse.get_pos()
      else:
         self.lastmouseposition = Inputs.mouse_position
      if self.ang >= 360: # Keeping angle within 360 degrees
         self.ang -= 360
      if self.ang < 0:
         self.ang += 360
      # self.ang = round(self.ang)
   def die(self):
      Game.entities = []
      for object in Sprite.sprites:
         try:
            object.playercheck()
         except:
            object.destroy()
            screen.fill((0,0,0))
            screen.blit(screen, (0,0))
      #games.screen.add(games.Text(value = "You Died!", size = 50, color = (255,0,0), x = screen_width // 2, y = screen_height // 2-50))
      self.text2 = "You blasted " + str(Game.kills) + " aliens."
      #games.screen.add(games.Text(value = self.text2, size = 50, color = (255,255,255), x = screen_width // 2, y = screen_height // 2))
         
     
   def shoot(self):
      self.xshoot = math.cos(math.radians((self.ang +(Player.FOV/2))%360)) * Game.bulletspeed
      self.yshoot = math.sin(math.radians((self.ang +(Player.FOV/2))%360)) * Game.bulletspeed
   
      Game.entities.append(Shot(self.xpos, self.ypos, self.xshoot, self.yshoot))
 
   def throwGren(self):
      self.xthrow = math.cos(math.radians(int((self.ang +(Player.FOV/2))%360))) * Game.grenspeed
      self.ythrow = math.sin(math.radians(int((self.ang +(Player.FOV/2))%360))) * Game.grenspeed
   
      Game.entities.append(Grenade(self.xpos, self.ypos, self.xthrow, self.ythrow))
 
   def throwSmoke(self):
      self.xthrow = math.cos(math.radians(int((self.ang +(Player.FOV/2))%360))) * Game.smokerspeed
      self.ythrow = math.sin(math.radians(int((self.ang +(Player.FOV/2))%360))) * Game.smokerspeed
   
      Game.entities.append(Smoker(self.xpos, self.ypos, self.xthrow, self.ythrow))
   
   def playercheck(self):
      pass
   
     
 
class GrenGui(Sprite):
   image = pygame.image.load("grenade.png")
   imagesize = 56
   color = (0,0,0)
   def __init__(self):
      super(GrenGui, self).__init__(image = GrenGui.image, right = -1 , bottom = -1)
      self.ability1overlay = pygame.Surface((GrenGui.imagesize, GrenGui.imagesize))
   def update(self):
      for play in Sprite.sprites:
         try:
            play.playercheck
            player = play
         except:
            pass
      self.ability1overlay.blit(self.image, (0,0))
      self.overheight = round(player.ability1cooldown / player.ability1maxcool * GrenGui.imagesize)
      if self.overheight:
         pygame.draw.rect(self.ability1overlay, GrenGui.color, (0, GrenGui.imagesize - self.overheight, GrenGui.imagesize, self.overheight), 0)
      screen.blit(self.ability1overlay, (10, screen_height // 2 - GrenGui.imagesize - 10))
class SmokeGui(Sprite):
   image = pygame.image.load("smoker.png")
   imagesize = 56
   color = (0,0,0)
   def __init__(self):
      super(SmokeGui, self).__init__(image = SmokeGui.image, right = -1, bottom = -1)
      self.ability2overlay = pygame.Surface((SmokeGui.imagesize, SmokeGui.imagesize))
   def update(self):
      for play in Sprite.sprites:
         try:
            play.playercheck
            player = play
         except:
            pass
      self.ability2overlay.blit(self.image, (0,0))
      self.overheight = round(player.ability2cooldown / player.ability2maxcool * SmokeGui.imagesize)
      if self.overheight:
         pygame.draw.rect(self.ability2overlay, SmokeGui.color, (0, SmokeGui.imagesize - self.overheight, SmokeGui.imagesize, self.overheight), 0)
      screen.blit(self.ability2overlay, (10, screen_height // 2 + 10))    
     
   
class Ray():
   def __init__(self,column,width):
      self.column = column
      self.width = width
      self.distance = 0
      self.color = (0,0,0)
      self.visible = True
   def draw(self):
      pygame.draw.rect(screen, self.color, (self.column, (screen_height//2)-((Draw.PROPORTION/self.distance)//2), self.width, Draw.PROPORTION/self.distance), 0)
     
class Draw(Sprite):
   image = pygame.image.load("crosshair.png")
   image.set_colorkey((255,255,255))
   # Colors
   red = (255, 0, 0)
   blue = (0, 0, 255)
   green = (0, 255, 0)
   white = (255, 255, 255)
   black = (0, 0, 0)
   gray = (130, 130, 130)
 
 
   BLOCK_SIZE = 200
   PROPORTION = 150000 # Proportion of distance to height
   SHADING = 4000 # Darkening of walls at distances
   PIX_PER_RAY = 3 # How many pixels for each ray, more means less lag
   def __init__(self):
      super(Draw, self).__init__(image = Draw.image, x = screen_width // 2, y = screen_height // 2)
      self.rainbow = [255, 0, 0]
      self.rainbow_pos = 0 # Point in rainbow's color

      self.COLORS = ("spacer", Draw.red, Draw.blue, Draw.green, Draw.white, self.rainbow) # List to use index to interpret wall from the map to color
     
      self.rays = [] # Lits of iterations of class Ray for each ray
      for j in range(0, 1080, self.PIX_PER_RAY):
         self.column = j
         self.wide = Draw.PIX_PER_RAY
         self.rays.append(Ray(self.column, self.wide))
   
   def update(self):
      for play in Sprite.sprites:
         try:
            play.playercheck
            player = play
         except:
            pass
 
      screen.fill((0,0,0))
      for j in range(screen_height//2): # Drawing roof and floor
         self.color = 130-(j*(130/(screen_height//2)))
         # pygame.draw.line(screen, (self.color, self.color, self.color), (0, j), (screen_width, j), 1)
         pygame.draw.line(screen, (self.color, self.color, self.color), (0, screen_height-j), (screen_width, screen_height-j), 1)
      for j in range(screen_width//Draw.PIX_PER_RAY): # Drawing rays
         self.ray_angle = player.ang +((Player.FOV/(screen_width//Draw.PIX_PER_RAY))*j) # Angle of current ray
         self.angle_offset = abs((Player.FOV/2 + player.ang) - self.ray_angle)# Diffrence in angle from center of screen
         self.angle_offset = round(self.angle_offset, 10)
         self.ray_angle = round(self.ray_angle, 10)
         self.ray_length, self.color = ray(self.ray_angle, player.xpos, player.ypos, self.angle_offset, Draw.BLOCK_SIZE) # Get ray length and wall color
         self.dist_mult = self.ray_length/Draw.SHADING # Get shading percent from distance and shading value (darkens wall farther from player)
         if self.dist_mult > 1: # Prevents dist_mult from reaching over 1
            self.dist_mult = 1
       
         self.rays[j].distance = self.ray_length
         self.rays[j].color = (self.COLORS[self.color][0]-(self.COLORS[self.color][0]*self.dist_mult), # R = wall color with shading from dist_mult
                            self.COLORS[self.color][1]-(self.COLORS[self.color][1]*self.dist_mult), # G = wall color with shading from dist_mult
                            self.COLORS[self.color][2]-(self.COLORS[self.color][2]*self.dist_mult)) # B = wall color with shading from dist_mult
      for object in Game.entities:
         object.get_updated(player.xpos, player.ypos, player.ang)
   
      self.things = self.rays + Game.entities
      self.order = [self.things[0]]
      for object in self.things[1:]:
         if object.visible:
            spotcheck = 0
            appended = False
            while not appended:
               if spotcheck == len(self.order):
                  self.order.append(object)
                  appended = True
               elif object.distance >= self.order[spotcheck].distance:
                  self.order.insert(spotcheck, object)
                  appended = True
               spotcheck += 1
      for object in self.order:
         object.draw()
      self.rainbow, self.rainbow_pos = update_rainbow(self.rainbow, self.rainbow_pos)
      screen.blit(Draw.image, (self.x,self.y))
     
def main():   
   draw = Draw()
   player = Player()
   
   
   grenadegui = GrenGui()
   smokergui = SmokeGui()
 
   pygame.event.set_grab(True)
   pygame.mouse.set_visible(False)
   
   Inputs.update()
   while (True):
      # Loop over pygame events
      for event in pygame.event.get():
         # If the screen should quit, quit.
         if event.type == QUIT or Inputs.keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
      print(Inputs.mouse_position)
      Inputs.update()
      Sprite.update_all()
      
      screen.blit(screen, (0,0))
      
      pygame.display.update()
      
      

   
main()
