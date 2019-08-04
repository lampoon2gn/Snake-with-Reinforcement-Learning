import random
import pygame
import numpy as np
import time
from pygame.locals import *
import cv2

#use a list of (x,y) to represent snake
class snake():
  __facing_options=[(1,0),(-1,0),(0,1),(0,-1)]

  def __init__(self,x_range,y_range):
    self.snake_list = [(random.randint(0,x_range),random.randint(0,y_range))]
    ran = random.randint(0, 3)#(1,0) means facing +x direction
    self.facing = self.__facing_options[ran] #initialize random facing
    self.got_apple = False
    self.num_of_moves = 0

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
      elif args[0] == 2: #keep moving
        pass
    else:
      for event in pygame.event.get():
        #keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
          pygame.quit()
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
      self.snake_list.insert(0,((self.snake_list[0][0]+int(self.facing[0]))%10,(self.snake_list[0][1]+int(self.facing[1]))%10))
      self.got_apple = False
    else:
      self.snake_list.insert(0,((self.snake_list[0][0]+int(self.facing[0]))%10,(self.snake_list[0][1]+int(self.facing[1]))%10))
      del self.snake_list[-1]
    self.num_of_moves +=1




class apple():
  def __init__(self,x_range,y_range,snake_object):
    while True:
      (x,y) = (random.randint(0,x_range) %10,random.randint(0,y_range-1)%10)
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
    #todo: change the hard coded 19,19 to number of rows
    apple_object.change_apple_position(9,9,snake_object)

def draw_grid(w, rows, surface):
  '''draw grid for game window, takes in width, rows, surface(pygame object)'''
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


class game():
  '''snake game'''
  GAME_GRID_DIMENSION = 100
  GAME_GRID_ROWS = 10
  
  def __init__(self):
    #create game window
    self.game_window = pygame.display.set_mode((self.GAME_GRID_DIMENSION, self.GAME_GRID_DIMENSION))
    #self.game_window = pygame.display.set_mode((500, 500),flags = 'SCALED')

    #create snake and apple
    self.s = snake(self.GAME_GRID_ROWS,self.GAME_GRID_ROWS)
    self.a = apple(self.GAME_GRID_ROWS,self.GAME_GRID_ROWS,self.s)
    #clock
    self.clock = pygame.time.Clock()
    #terminal state
    self.terminal = False
    self.reward = 0

  def bytearray_to_rgb(self,data):
    r=[]
    g=[]
    b=[]
    for i in range(100):
      #r.append(data[300*i:300*(i+1):3])
      g.append(data[300*i+1:300*(i+1)+1:3])
      #b.append(data[300*i+2:300*(i+1)+2:3])
    return np.array(g).reshape(1,100,100)

  def get_env(self):
    '''return list(image),facing,reward,terminal'''
    data = np.asarray(list(pygame.image.tostring(self.game_window, 'RGB')))
    data = self.bytearray_to_rgb(data)
    return data,self.s.facing,len(self.s.snake_list)-1-self.s.num_of_moves*0.01,self.terminal

  def run_game(self,*args):
    '''run snake game for one frame if imported. Uncomment "while True:" and "self.clock.tick(10)" to play the game'''
    #while True:
      #pygame.time.delay(50)
      #self.clock.tick(10)
    self.terminal = False
    if args:
      self.s.apply_action(args[0])
    else:
      self.s.apply_action()
    score = detect_collision(self.a,self.s)
    #terminate condition
    if score:
      #print("Score: " + str(score))
      self.s = snake(self.GAME_GRID_ROWS,self.GAME_GRID_ROWS)
      self.terminal = True
      score = 0

    draw_all(self.game_window,self.s,self.a,self.GAME_GRID_DIMENSION,self.GAME_GRID_ROWS)
    pygame.display.update()




if __name__ == "__main__":
  gam = game()
  gam.run_game()
  