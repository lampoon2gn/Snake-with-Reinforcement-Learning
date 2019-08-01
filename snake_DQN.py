import numpy as np
import random
import math
#from scores.score_logger import ScoreLogger
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import time

from snake_game import *


gamma =0.90
learning_rate=0.0007

mem_size =100000
batch_size=32
explore_max = 1
explore_min = 0.000001
explore_decay=0.999

class DQN:

  def __init__(self,input_dimension):
    self.exploration_rate = explore_max
    self.action_list = [-1,0,1]
    self.memory =deque(maxlen=mem_size)

    #NN stuff
    self.model = Sequential()
    self.model.add(Dense(24, input_shape=(input_dimension,), activation="relu"))
    self.model.add(Dense(24, activation="relu"))
    self.model.add(Dense(24, activation="relu"))
    self.model.add(Dense(3, activation="linear"))
    self.model.compile(loss="mse", optimizer=Adam(lr=learning_rate))

  def remember(self,state,action,reward,next_state,done):
    self.memory.append((state,action,reward,next_state,done))

  #explore randomly or use NN to get an action
  def get_action(self,state):
    if np.random.rand() < self.exploration_rate:
      return random.randrange(self.action_list)
    Q = self.model.predict(state)
    return np.argmax(Q[0])

  def experience_replay(self):
    if len(self.memory) < batch_size:
      return
    batch = random.sample(self.memory,batch_size)
    for state,action,reward,state_next,terminal in batch:
      Q_update = reward
      if not terminal:
        Q_update = (reward + gamma *np.amax(self.model.predict(state_next)[0]))
      Q = self.model.predict(state)
      Q[0][action] =Q_update
      self.model.fit(state,Q,verbose=0)
    self.exploration_rate *= explore_decay
    self.exploration_rate =max(explore_min,self.exploration_rate) 


def snake_agent():
  env = game()
  #solver = DQN(12000)
  prev_reward = 0

  run = 0
  while True:
    run += 1
    while True:
      env.run_game()
      state = data1,facing,reward = env.get_env()
      print("run_1: face: {} reward:{} position:{}".format(str(facing),str(reward),str(env.s.snake_list[0])))
      env.run_game(1)
      next_state = data2,facing,reward = env.get_env()
      print("run_2: face: {} reward:{} position:{}".format(str(facing),str(reward),str(env.s.snake_list[0])))

      time.sleep(100)

      if prev_reward > reward:
        reward = -prev_reward
        x=input()
      print(facing,str(reward))
      prev_reward = reward
      #action = solver.get_action(state)
  #     state_next,reward,terminal,info = env.step(action)
  #     reward = reward if not terminal else -reward
  #     state_next = np.reshape(state_next, [1, observation_space])
  #     solver.remember(state,action,reward,state_next,terminal)
  #     state = state_next
  #     if terminal:
  #       print ("Run: " + str(run) + ", exploration: " + str(solver.exploration_rate) + ", score: " + str(step))
  #       break
  #     solver.experience_replay()

if __name__ == "__main__":
  snake_agent()