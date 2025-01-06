from SnakeAI import SnakeGame
import numpy as np
import torch
import time
import random
from collections import deque
from network import Linear_QNet, QTrainer
import pygame

# input -> [1,0,0,0] -> fruit -> [1,0,0,1] -> danger -> [1,0,0,0]

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class PlayAI:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    def SetSnake(self,snake,newx,newy):
        snake.x = newx
        snake.y = newy
        return snake

    def GetReqState(self,state,snakegame):
        snake,fruit,snakebody,movement = state

        aistate = [
            movement[0],
            movement[1],
            movement[2],
            movement[3],

            snake.y < fruit.y,
            snake.y > fruit.y,
            snake.x < fruit.x,
            snake.x > fruit.x,

            (movement[0] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x,snake.y - snakegame.block))) or
            (movement[1] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x,snake.y + snakegame.block))) or
            (movement[2] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x - snakegame.block,snake.y))) or
            (movement[3] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x + snakegame.block,snake.y))) ,

            (movement[0] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x - snakegame.block,snake.y))) or
            (movement[1] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x + snakegame.block,snake.y))) or
            (movement[2] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x,snake.y + snakegame.block))) or
            (movement[3] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x,snake.y - snakegame.block))) ,

            (movement[0] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x + snakegame.block,snake.y))) or
            (movement[1] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x - snakegame.block,snake.y))) or
            (movement[2] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x,snake.y - snakegame.block))) or
            (movement[3] == 1 and snakegame.CheckCollisions(self.SetSnake(snake,snake.x,snake.y + snakegame.block))) ,

        ]
        
        return np.array(aistate,dtype=int)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        #self.epsilon = 80 - self.n_games
        self.epsilon = 1000
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            print(state0)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move    


if __name__ == "__main__":
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = PlayAI()
    snakegame = SnakeGame()
    game_state = snakegame.GetState()
    while True:
        state = agent.GetReqState(game_state,snakegame)
        final_move = agent.get_action(state)
        isgameover,iseaten,new_state = snakegame.PlayGame(final_move,game_state)
        if isgameover:
            new_state = snakegame.Reset()
        snakegame.Render(new_state,iseaten,isgameover) 
        pygame.time.Clock().tick(20)
        game_state = new_state

        new_ai_state = agent.GetReqState(new_state,snakegame)
        reward = 0
        if(iseaten):
            reward = 10
        if(isgameover):
            reward = -10
        agent.train_short_memory(state, final_move, reward, new_ai_state, isgameover)

        agent.remember(state, final_move, reward, new_ai_state, isgameover)

        if isgameover:
            # train long memory, plot result
            agent.n_games += 1
            agent.train_long_memory()
        

        

