import pygame
import time
import sys
class User1:
    attacks = [1,2,3];
    properties = {"name":"KKH","status":0,"energy":0}
    old_properties = {"name":"KKH","status":0,"energy":0}
    # -1 :막기
    # 0 : 으
    # 1 : 파
    # 2 : 에너지파 3>>1 그러나,막기로 막을 수 있음
    # 3 : 원기옥 
    # 기 상태
    strategy = [0,0,1];
    def __init__(self):
        pass
    def next_step(self,step):
        # 정의해야 할 Method
        # 아래 코드는 건들지 말 것
        try:
            self.properties['status'] = self.strategy[step]
            if self.properties['status'] == 0:
                self.properties['energy']+=1;
            elif self.properties['status'] in self.attacks:
                if self.properties['energy'] < self.properties['status']:
                    self.properties['status'] = 0;
                    self.properties['energy']+=1;
                else:
                    self.properties['energy']-=self.properties['status'];
        except:
            print(self.properties['name']+"Lose!");
            sys.exit();
    def setOther(self,other):
        self.otherProperties = other.old_properties
    def afterTurn(self):
        for i in self.old_properties:
            self.old_properties[i] = self.properties[i];
class User2:
    attacks = [1,2,3];
    properties = {"name":"SHS","status":0,"energy":0}
    old_properties = {"name":"SHS","status":0,"energy":0}
    # -1 :막기
    # 0 : 으
    # 1 : 파
    # 2 : 에너지파 3>>1 그러나,막기로 막을 수 있음
    # 3 : 원기옥 
    # 기 상태
    strategy = [0,0,1,0];
    def __init__(self):
        pass
    def next_step(self,step):
        # 정의해야 할 Method
        # 아래 코드는 건들지 말 것
        try:
            self.properties['status'] = self.strategy[step]
            if self.properties['status'] == 0:
                self.properties['energy']+=1;
            elif self.properties['status'] in self.attacks:
                if self.properties['energy'] < self.properties['status']:
                    self.properties['status'] = 0;
                    self.properties['energy']+=1;
                else:
                    self.properties['energy']-=self.properties['status'];
        except:
            print(self.properties['name']+"Lose!");
            sys.exit();
    def setOther(self,other):
        self.otherProperties = other.old_properties
    def afterTurn(self):
        for i in self.old_properties:
            self.old_properties[i] = self.properties[i];
            
            
user1 = User1();
user2 = User2();
user1.setOther(user2);
user2.setOther(user1);


pygame.init()
 
display_width = 800
display_height = 600
 
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255) 
block_color = (53,115,255)
 
car_width = 73
i=0;
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('DragonBall')
clock = pygame.time.Clock()
 
user1_image = pygame.image.load('user1_0.jpg')
user2_image = pygame.image.load('user2_0.jpg')
user1_image = pygame.transform.scale(user1_image, (200, 100))
user2_image = pygame.transform.scale(user2_image, (200, 100))
  
def display():
    x1 = (display_width * 0.2);
    y1 = (display_height * 0.1);
    x2 = (display_width * 0.7);
    y2 = (display_height * 0.1);
    gameDisplay.blit(user1_image,(x1,y1))
    gameDisplay.blit(user2_image,(x2,y2))
    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
 
    pygame.display.update()
 
    time.sleep(2)
 
    game_loop()
    
    
 
def crash():
    message_display('You Crashed')

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Dragon ball", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,blue,game_loop)
        button("Quit",550,450,100,50,red,blue,game_loop)

        pygame.display.update()
        clock.tick(15)
        
        
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)  

def button2(msg,x,y,w,h,ic,ac,action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    
def game_main():
    global i;
    attacks = [1,2,3];
    user1.next_step(i);
    user2.next_step(i);
    display();
    print(user1.properties['name']+' : '+str(user1.properties['status'])+' VS '+user2.properties['name']+' : '+str(user2.properties['status']));
    if user1.properties['status'] !=user2.properties['status']:
        if user1.properties['status'] == 3:
            print(user1.properties['name']+" Win!");
        elif user2.properties['status'] ==3:
            print(user2.properties['name']+" Win!")
            
        if(user1.properties['status'] in attacks)and(user2.properties['status'] in attacks):
            if user1.properties['status'] < user2.properties['status']:
                print(user2.properties['name']+" Win!");
            elif user1.properties['status'] > user2.properties['status']:
                print(user1.properties['name']+" Win!")
            else :
                pass
        if (user1.properties['status'] ==0 and (user2.properties['status'] in attacks))|((user1.properties['status'] in attacks) and user2.properties['status']==0):
            if user1.properties['status'] ==0:
                print(user2.properties['name']+" Win!")
            else:
                print(user1.properties['name']+" Win!")
    user1.afterTurn();
    user2.afterTurn();
    i+=1;
def game_loop():
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_LEFT:
#                    x_change = -5
#                if event.key == pygame.K_RIGHT:
#                    x_change = 5
# 
#            if event.type == pygame.KEYUP:
#                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#                    x_change = 0
# 
#        x += x_change
        gameDisplay.fill(white)
 
        button2("GO!",150,450,100,50,green,blue,game_main)
        clock.tick(0)

game_intro()
game_loop()
pygame.quit()
quit()