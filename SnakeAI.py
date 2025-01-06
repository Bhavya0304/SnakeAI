import pygame
from pygame.locals import *
import time
import random
from pygame.font import Font


class SnakeGame:
    def __init__(self):
        self.block = 15
        self.heightratio = 15
        self.widthratio = 30
        self.size = self.widthratio*self.block,self.heightratio*self.block
        self.width,self.height = self.size
        self.running = True
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((0,0,0))
        self.snake = pygame.Rect(0,0,self.block,self.block)
        self.snakebody = []
        self.score = 0
        self.movement = [0,0,0,1] # up, down, left, right
        self.action = [1,0,0] # straight, left, right
        self.fruit = self.PutFruit()
        pygame.init()
    
    def PutFruit(self):
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        x = self.GetInRange(x,self.block)
        y = self.GetInRange(y,self.block)
        fruit = pygame.Rect(x,y,self.block,self.block)
        return fruit

    def PlaceSnake(self):
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        x = self.GetInRange(x,self.block)
        y = self.GetInRange(y,self.block)
        snake = pygame.Rect(x,y,self.block,self.block)
        return snake

    def Reset(self):
        snake = self.PlaceSnake()
        snakebody = []
        action = [1,0,0]
        movement = [0,0,0,1]
        fruit = self.PutFruit()
        self.score = 0
        return snake,fruit,snakebody,movement
    
    def ShowScore(self,score):
        fonts = pygame.font.Font(size=20)
        text_surface = fonts.render("Score: " + str(score), True,(255,255,255))
        self.screen.blit(text_surface,(0,0))

    def RenderSnakeBody(self,snakehead : pygame.Rect,snakebody:list[pygame.Rect]):
        n = len(snakebody)
        newbody = snakebody
        if len(newbody) > 0:
            for i in range(n-1,0,-1):
                newbody[i].x = newbody[i-1].x 
                newbody[i].y = newbody[i-1].y 
            newbody[0].x = snakehead.x
            newbody[0].y = snakehead.y
        return newbody      

    def GetInRange(self,x,rangein):
        diff = x % rangein
        if (x - diff < 0):
            x = x + diff
        else:
            x = x - diff 
        return x

    def GetState(self):
        return self.snake,self.fruit,self.snakebody,self.movement

    def UpdateState(self,state):
        self.snake,self.fruit,self.snakebody,self.movement = state

    def CheckCollisions(self,snake):
            if(snake.x < 0 or snake.x >= self.width):
              
                return True
            elif (snake.y >= self.height or snake.y < 0):
              
                return True
            else:
                return False  

    def HasEaten(self,snakehead,fruit):
        return snakehead.centerx == fruit.centerx and fruit.centery == snakehead.centery

    def IncreaseSnake(self,snakebody:list[pygame.Rect],snakehead):
        if(len(snakebody) == 0):
            if(self.movement[0] > 0 or self.movement[1] > 0):
                newbody = pygame.Rect(0,0,self.block,self.block)
                newbody.x = snakehead.x + self.block
                newbody.y = snakehead.y
                snakebody.append(newbody)

            else:
                newbody = pygame.Rect(0,0,self.block,self.block)
                newbody.x = snakehead.x - self.block   
                newbody.y = snakehead.y
                snakebody.append(newbody)
        else:
            if(self.movement[0] > 0 or self.movement[1] > 0):
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
    
    def PlayGame(self,action,state):
        snakehead,fruit,snakebody,movement = state
        if action[0] == 1:
            if movement[2] == 1:
                snakehead.x -= self.block     
            elif movement[3] == 1:
                snakehead.x += self.block
            elif movement[0] == 1:
                snakehead.y -= self.block
                movement = [1,0,0,0]  
            elif movement[1] == 1:
                snakehead.y += self.block
                movement = [0,1,0,0]  
        if action[1] == 1:
            if movement[2] == 1:
                snakehead.y += self.block
                movement = [0,1,0,0]     
            elif movement[3] == 1:
                snakehead.y -= self.block
                movement = [1,0,0,0] 
            elif movement[0] == 1:
                snakehead.x -= self.block
                movement = [0,0,1,0] 
            elif movement[1] == 1:
                snakehead.x += self.block 
                movement = [0,0,0,1]     
        if action[2] == 1:
            if movement[2] == 1:
                snakehead.y -= self.block
                movement = [1,0,0,0]     
            elif movement[3] == 1:
                snakehead.y += self.block
                movement = [0,1,0,0]     
            elif movement[0] == 1:
                snakehead.x += self.block
                movement = [0,0,0,1]     
            elif movement[1] == 1:
                snakehead.x -= self.block
                movement = [0,0,1,0]     
        isgameover = self.CheckCollisions(snakehead)
        iseaten = self.HasEaten(snakehead,fruit)
        if(iseaten):
            snakebody = self.IncreaseSnake(snakebody,snakehead)
            fruit = self.PutFruit()

        return isgameover,iseaten,[snakehead,fruit,snakebody,movement]

    def Render(self,state,iseaten,gameover):
        self.screen.fill((0,0,0))
        if iseaten:
            self.score += 1

        self.ShowScore(self.score)
        snakehead,fruit,snakebody,movement = state    
        snakebody = self.RenderSnakeBody(snakehead,snakebody)

        for i,body in enumerate(self.snakebody):  
            pygame.draw.rect(self.screen,(255,0,0),body)

        pygame.draw.rect(self.screen,(255,0,0),snakehead) 
        pygame.draw.rect(self.screen,(0,255,0),fruit)
        #Render Snake Body
        
        pygame.display.flip()
        self.UpdateState([snakehead,fruit,snakebody,movement])
    
    def StateGet(self,state):
        snake,fruit,snakebody,movement = state
        return dict(snake=snake,fruit=fruit,snakebody=snakebody,movement=movement)

    def HumanFeedback(self,action,movement):
        retaction = [1,0,0]
        if action == pygame.K_DOWN:
            if movement[0] == 1 or movement[1] == 1:
                retaction = [1,0,0]
            elif movement[2] == 1:
                retaction = [0,1,0]
            elif movement[3] == 1:
                retaction = [0,0,1]
        elif action == pygame.K_UP:
            if movement[0] == 1 or movement[1] == 1:
                retaction = [1,0,0]
            elif movement[2] == 1:
                retaction = [0,0,1]
            elif movement[3] == 1:
                retaction = [0,1,0]
        elif action == pygame.K_RIGHT:
            if movement[2] == 1 or movement[3] == 1:
                retaction = [1,0,0]
            elif movement[0] == 1:
                retaction = [0,0,1]
            elif movement[1] == 1:
                retaction = [0,1,0]
        elif action == pygame.K_LEFT:
            if movement[2] == 1 or movement[3] == 1:
                retaction = [1,0,0]
            elif movement[0] == 1:
                retaction = [0,1,0]
            elif movement[1] == 1:
                retaction = [0,0,1]
        return retaction
            

if __name__ == "__main__":
    snakegame = SnakeGame()
    state = snakegame.GetState()
    while True:
        time.sleep(0.1)
        action = [1,0,0]
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    action = snakegame.HumanFeedback(event.key,snakegame.StateGet(state)['movement'])
        # randommove = random.randint(0,2)
        # arr = [0,0,0]
        # arr[randommove] = 1
        isgameover,iseaten,state = snakegame.PlayGame(action,state)
        if isgameover:
            state = snakegame.Reset()
        snakegame.Render(state,iseaten,isgameover)     


