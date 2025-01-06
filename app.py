import pygame
from pygame.locals import *
import time
import random
from pygame.font import Font


#pygame.init()


class SnakeGame:

    def __init__(self):
        self.size = 720,330
        self.width,self.height = self.size
        self.running = True
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((0,0,0))
        self.block = 15
        self.snake = pygame.Rect(0,0,self.block,self.block)
        self.snakebody = []
        self.score = 0
        self.movement = [self.block,0]
        pygame.init()


    def getState(self):
        state = [0,0,0,0,0,0,0,0,0,0,0]
    
        pass

    def reward(self,action):
        pass

    def isGameover(self):
        pass

    def reset(self):
        pass

    def IncreaseSnake(self,snakebody:list[pygame.Rect],snakehead):
        if(len(snakebody) == 0):
            newbody = pygame.Rect(0,0,self.block,self.block)
            newbody.x = snakehead.x
            newbody.y = snakehead.y
            snakebody.append(newbody)
        else:
            if(self.movement[0] > 0):
                newbody = pygame.Rect(0,0,self.block,self.block)
                newbody.x = snakebody[len(snakebody) - 1].x + self.block
                newbody.y = snakebody[len(snakebody) - 1].y
                snakebody.append(newbody)

            else:
                newbody = pygame.Rect(0,0,self.block,self.block)
                newbody.x = snakebody[len(snakebody) - 1].x - self.block   
                newbody.y = snakebody[len(snakebody) - 1].y
                snakebody.append(newbody)

        return snakebody

    def HasEaten(self,snakehead,fruit):
        return snakehead.centerx == fruit.centerx and fruit.centery == snakehead.centery

    def RenderSnakeBody(self,snakehead : pygame.Rect,snakebody:list[pygame.Rect]):
        n = len(snakebody)
        if len(snakebody) > 0:
            for i in range(n-1,0,-1):
                snakebody[i].x = snakebody[i-1].x 
                snakebody[i].y = snakebody[i-1].y 
            snakebody[0].x = snakehead.x
            snakebody[0].y = snakehead.y
            for i,body in enumerate(snakebody):  
                pygame.draw.rect(self.screen,(255,0,0),body)  

    def GetInRange(self,x,rangein):
        diff = x % rangein
        if (x - diff < 0):
            x = x + diff
        else:
            x = x - diff 
        return x       

    def PutFruit(self):
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        x = self.GetInRange(x,self.block)
        y = self.GetInRange(y,self.block)
        fruit = pygame.Rect(x,y,self.block,self.block)
        return fruit

    def ChangeMovement(self,action,movement):
        if action == pygame.K_LEFT: # left
            movement[0] = -self.block
            movement[1] = 0
        elif action == pygame.K_RIGHT: # right
            movement[0] = self.block
            movement[1] = 0
        elif action == pygame.K_UP: # up
            movement[0] = 0
            movement[1] = -self.block
        elif action == pygame.K_DOWN: # down
            movement[0] = 0
            movement[1] = self.block 
        return movement       
    
    def GameOver(self):
        fonts = Font(size=30)
        while True:
            text_surface = fonts.render("Press space bar to play again", True,(255,255,255))
            
            self.screen.blit(text_surface,(220,120))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True

    def ShowScore(self):
        fonts = pygame.font.Font(size=20)
        text_surface = fonts.render("Score: " + str(self.score), True,(255,255,255))
        self.screen.blit(text_surface,(0,0))

    def UpdateState(self,action):
        self.screen.fill((0,0,0))
        self.movement = self.ChangeMovement(action,self.movement)

        pass

    def CheckCollisions(self):
            if(self.snake.left < 0 or self.snake.right > self.width):
                return True
            elif (self.snake.bottom > self.height or self.snake.top < 0):
                return True
            else:
                return False                
    #State -> self.snakehead
    def Render(self,state):
        self.screen.fill((0,0,0))

        pass

    def PlayAction(self,action):
        pass

    def PlayGame(self):   
        # place after play game if won == true        
        self.fruit = self.PutFruit()
        # Remove
        while self.running:
            # place it in render
            eaten = self.HasEaten(self.snake,self.fruit)
            if(eaten):
                self.fruit = self.PutFruit()
                self.snakebody = self.IncreaseSnake(self.snakebody,self.snake)
                self.score += 1
            self.ShowScore()
            self.RenderSnakeBody(self.snake,self.snakebody)   

            #Change Movements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.movement = self.ChangeMovement(event.key,self.movement)  
                    print(self.movement)
            # Collisons
            if(self.snake.left < 0 or self.snake.right > self.width):
                status = self.GameOver()
                if(status):
                    self.screen.fill((0,0,0))
                    self.movement = [self.block,0]
                    self.snake.x = 0
                    self.snake.y = 0
                    self.snakebody = []
                else:
                    self.running = False    
            elif(self.snake.bottom > self.height or self.snake.top < 0):
                status = self.GameOver()
                if(status):
                    self.screen.fill((0,0,0))
                    self.movement = [self.block,0]
                    self.snake.x = 0
                    self.snake.y = 0
                    self.snakebody = []

                else:
                    running = False  
            

            # Move forward
            self.snake.x += self.movement[0]
            self.snake.y += self.movement[1]

            pygame.draw.rect(self.screen,(255,0,0),self.snake)  
            pygame.draw.rect(self.screen,(0,255,0),self.fruit)  
            #self.screen.blit(snakehead,snake)
            time.sleep(0.1)
            pygame.display.update()
        pygame.quit()   


game = SnakeGame()

game.PlayGame()
 