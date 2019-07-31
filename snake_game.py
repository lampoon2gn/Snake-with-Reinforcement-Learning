import random
import pygame
#import cv2
from pygame.locals import *


#use a list of (x,y) to represent snake
class snake():
  __facing_options=[(1,0),(-1,0),(0,1),(0,-1)]

  def __init__(self,x_range,y_range):
    self.snake_list = [(random.randint(0,x_range),random.randint(0,y_range))]
    ran = random.randint(0, 3)#(1,0) means facing +x direction
    self.facing = self.__facing_options[ran] #initialize random facing
    self.got_apple = False

  def apply_action(self,*args):
    '''find out what direction the snake will be facing after the action and move snake once'''
    if args:
      if args[0] == 1: #right
        if self.facing[0] == 0: #originally moving in +/-y direction  
          self.facing = self.facing[::-1]
          self.facing = (-self.facing[0],self.facing[1])
        else: #originally moving in +/-y direction
          self.facing = self.facing[::-1]

      elif args[0] == 0: #left
        if self.facing[0] == 0:
          self.facing = self.facing[::-1]
        else:
          self.facing = self.facing[::-1]
          self.facing = (-self.facing[0],self.facing[1])
    else:
      for event in pygame.event.get():
        #keys = pygame.key.get_pressed()
        if event.type == KEYDOWN:
          if event.key == pygame.K_RIGHT:#keys[pygame.K_LEFT]:
            if self.facing[0] == 0: #originally moving in +/-y direction  
              self.facing = self.facing[::-1]
              self.facing = (-self.facing[0],self.facing[1])
            else: #originally moving in +/-y direction
              self.facing = self.facing[::-1]

          elif event.key == pygame.K_LEFT:#keys[pygame.K_RIGHT]:
            if self.facing[0] == 0:
              self.facing = self.facing[::-1]
            else:
              self.facing = self.facing[::-1]
              self.facing = (self.facing[0],-self.facing[1])

    self.move_snake()

  def move_snake(self):
    '''add new cube in the direction the snake is facing, and chop off the tail(keep tail if got_apple)'''
    if self.got_apple:
      self.snake_list.insert(0,((self.snake_list[0][0]+int(self.facing[0]))%20,(self.snake_list[0][1]+int(self.facing[1]))%20))
      self.got_apple = False
    else:
      self.snake_list.insert(0,((self.snake_list[0][0]+int(self.facing[0]))%20,(self.snake_list[0][1]+int(self.facing[1]))%20))
      del self.snake_list[-1]




class apple():
  def __init__(self,x_range,y_range,snake_object):
    while True:
      (x,y) = (random.randint(0,x_range),random.randint(0,y_range))
      if (x,y) not in snake_object.snake_list:
        break
    self.position = (x,y)

  def change_apple_position(self,x_range,y_range,snake_object):
    while True:
      (x,y) = (random.randint(0,x_range),random.randint(0,y_range))
      if (x,y) not in snake_object.snake_list:
        break
    self.position = (x,y)


def detect_collision(apple_object,snake_object):
  '''detect if snake ran into self/got apple'''
  snake_set = set(snake_object.snake_list) #use set to eliminate duplicate,duplicate means collision
  if len(snake_set) != len(snake_object.snake_list):
    '''game over, return score'''
    return len(snake_set)
  if apple_object.position in snake_object.snake_list:
    '''got an apple, keep tail next time snake moves,and generate new apple'''
    snake_object.got_apple = True
    apple_object.change_apple_position(19,19,snake_object)

def draw_grid(w, rows, surface):
  '''draw grid for game window'''
  pass
  # sizeBtwn = w // rows
  # x = 0
  # y = 0
  # for l in range(rows):
  #   x = x + sizeBtwn
  #   y = y + sizeBtwn
  #   pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
  #   pygame.draw.line(surface, (255,255,255), (0,y),(w,y))

def draw_snake_apple(surface,snake_object,apple_object,dimension,rows):
  '''draw snake and apple on game window'''
  dis = dimension // rows
  #draw apple
  pygame.draw.rect(surface, (255,255,0), (apple_object.position[0]*dis+1,apple_object.position[1]*dis+1, dis-2, dis-2))
  #draw snake
  for tup in snake_object.snake_list:
    pygame.draw.rect(surface, (255,255,255), (tup[0]*dis+1,tup[1]*dis+1, dis-2, dis-2))

def draw_all(surface,snake_object,apple_object,dimension,rows):
  surface.fill((0,0,0))
  draw_snake_apple(surface,snake_object,apple_object,dimension,rows)
  draw_grid(dimension,rows,surface)
  pygame.display.set_caption(str(len(snake_object.snake_list)))


def run_game():
  GAME_GRID_DIMENSION = 200
  GAME_GRID_ROWS = 20
  #create game window
  game_window = pygame.display.set_mode((GAME_GRID_DIMENSION, GAME_GRID_DIMENSION))
  #create snake and apple
  s = snake(GAME_GRID_ROWS,GAME_GRID_ROWS)
  a = apple(GAME_GRID_ROWS,GAME_GRID_ROWS,s)
  #clock
  clock = pygame.time.Clock()

  def get_env():
    '''return env,facing,reward'''
    data = list(pygame.image.tostring(game_window, 'RGB'))
    return data,s.facing,len(s.snake_list)

  while True:
    pygame.time.delay(50)
    clock.tick(10)
    #print(s.snake_list)

    s.apply_action()
    score = detect_collision(a,s)

    #data = get_env()
    #print(len(data[0]))
    #x=input()

    #terminate condition
    if score:
      print("Score: " + str(score))
      s = snake(GAME_GRID_ROWS,GAME_GRID_ROWS)

    draw_all(game_window,s,a,GAME_GRID_DIMENSION,GAME_GRID_ROWS)
    
    pygame.display.update()




#if __name__ == "__main__":
#main()
  