import random
import numpy as np
import time
import keyboard as kbd
import os
import matplotlib.cm as cm
from matplotlib import pyplot as plt
import matplotlib.animation as animation


#use a list of (x,y) to represent snake
class snake():
  __facing_options=[(1,0),(-1,0),(0,1),(0,-1)]

  def __init__(self,x_range,y_range):
    self.snake_list = [(random.randint(0,x_range-1),random.randint(0,y_range-1))]
    ran = random.randint(0, 3)#(1,0) means facing +x direction
    self.facing = self.__facing_options[ran] #initialize random facing
    self.got_apple = False
    self.num_of_moves = 0
    self.reward = 0
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
      if kbd.is_pressed('esc'):
        exit()
      elif kbd.is_pressed('right'):
        if self.facing[0] == 0: #originally moving in +/-y direction  
          self.facing = self.facing[::-1]
          self.facing = (-self.facing[0],self.facing[1])
        else: #originally moving in +/-y direction
          self.facing = self.facing[::-1]
      elif kbd.is_pressed('left'):
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
      self.num_of_moves = 0
      self.got_apple = False
    else:
      self.snake_list.insert(0,((self.snake_list[0][0]+int(self.facing[0]))%10,(self.snake_list[0][1]+int(self.facing[1]))%10))
      del self.snake_list[-1]
    self.num_of_moves +=1


class apple():
  def __init__(self,x_range,y_range,snake_object):
    self.x_range = x_range
    self.y_range = y_range
    while True:
      (x,y) = (random.randint(0,x_range-1),random.randint(0,y_range-1))
      if (x,y) not in snake_object.snake_list:
        break
    self.position = (x,y)

  def change_apple_position(self,snake_object):
    while True:
      (x,y) = (random.randint(0,self.x_range-1),random.randint(0,self.y_range-1))
      if (x,y) not in snake_object.snake_list:
        break
    self.position = (x,y)


def detect_collision(apple_object,snake_object):
  '''detect if snake ran into self/got apple'''
  snake_set = set(snake_object.snake_list) #use set to eliminate duplicate,duplicate means collision
  if len(snake_set) != len(snake_object.snake_list):
    '''game over'''
    return True
  if apple_object.position in snake_object.snake_list:
    '''got an apple, keep tail next time snake moves,and generate new apple'''
    snake_object.got_apple = True
    snake_object.reward = 1

    apple_object.change_apple_position(snake_object)

def draw_all(surface,snake_object,apple_object,dimension,rows):
  '''draw snake and apple on game window'''
  #draw apple
  surface[apple_object.position[1]][apple_object.position[0]] = .5
  #draw snake
  for tup in snake_object.snake_list:
    surface[tup[1]][tup[0]] = 1




class game():
  '''snake game'''
  GAME_GRID_DIMENSION = 10
  GAME_GRID_ROWS = 10
  flag = 1
  def __init__(self):
    #create game window
    self.game_window = np.zeros((self.GAME_GRID_ROWS,self.GAME_GRID_ROWS))

    #create snake and apple
    self.s = snake(self.GAME_GRID_ROWS,self.GAME_GRID_ROWS)
    self.a = apple(self.GAME_GRID_ROWS,self.GAME_GRID_ROWS,self.s)
    #terminal state
    self.terminal = False


  def get_env(self):
    '''return list(image),facing,reward,terminal'''
    data = self.game_window
    reward = self.s.reward
    self.s.reward = 0
    return data.flatten().reshape(1,100),self.s.facing,reward,self.terminal,len(self.s.snake_list)

  def show_window(self):
    lst = str(self.game_window)
    lst = lst.replace('0',' ')
    lst = lst.replace('1','x')
    lst = lst.replace('0.5','O')
    print(lst)


  def run_game(self,*args):
    '''run snake game for one frame.'''
    #while True:
    self.game_window = np.zeros((self.GAME_GRID_ROWS,self.GAME_GRID_ROWS))
    #time.sleep(1)
    done = False
    self.terminal = False
    if args:
      self.s.apply_action(args[0])
    else:
      self.s.apply_action()
    draw_all(self.game_window,self.s,self.a,self.GAME_GRID_DIMENSION,self.GAME_GRID_ROWS)
    done = detect_collision(self.a,self.s)
    #terminate condition
    if done:
      #print("Score: " + str(score))
      #self.s = snake(self.GAME_GRID_ROWS,self.GAME_GRID_ROWS)
      self.terminal = True
      

    
    
    #os.system('cls') 
    #self.show_window()
    #plt.pause(0.0001)


    
    #time.sleep(10)



if __name__ == "__main__":
  gam = game()
  gam.run_game()
  