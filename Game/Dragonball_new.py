import pygame
import time
import random
import sys 

pygame.init()
 
display_width = 800
display_height = 600
 
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53,115,255)
isFinished = False;
i=0;
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()


user1_image = pygame.image.load('user1_0.jpg')
user2_image = pygame.image.load('user1_0.jpg')
user1_image = pygame.transform.scale(user1_image, (200, 250))
user2_image = pygame.transform.scale(user2_image, (200, 250))
user1_image = pygame.transform.flip(user1_image, 1, 0)
user2_image = pygame.transform.flip(user1_image, 1, 0)

def display():
    attacks = [1,2,3];
    if not isFinished:
        x1 = (display_width * 0.1);
        y1 = (display_height/2)-100;
        x2 = (display_width * 0.65);
        y2 = (display_height/2)-100;
        gameDisplay.blit(user1_image,(x1,y1))
        gameDisplay.blit(user2_image,(x2,y2))
        global i;
        SmallText = pygame.font.Font('NanumGothic.ttf',30)
        text1 = user1.properties['name']+' : '+user1.show_status()+' VS '+user2.properties['name']+' : '+user2.show_status()
        TextSurf1, TextRect1 = text_objects(text1, SmallText)
        TextRect1.center = ((display_width/2),(display_height/2-200))
        gameDisplay.blit(TextSurf1, TextRect1)
        text2 = "Turn"+str((i))
        TextSurf2, TextRect2 = text_objects(text2, SmallText)
        TextRect2.center = ((display_width/2),(display_height/2-250))
        gameDisplay.blit(TextSurf2, TextRect2)
        text3 = "Energy : "+user1.properties['name']+' = '+user1.show_energy()+' VS '+user2.properties['name']+' = '+user2.show_energy()
        TextSurf3, TextRect3 = text_objects(text3, SmallText)
        TextRect3.center = ((display_width/2),(display_height/2-150))
        gameDisplay.blit(TextSurf3, TextRect3)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        text = "VS"
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
    else:
        if user1.properties['status'] !=user2.properties['status']:
            if user1.properties['status'] == 3:
                text = user1.properties['name']+" Win!"
                largeText = pygame.font.Font('HUDaku.ttf',115)
                TextSurf, TextRect = text_objects(text, largeText)
                TextRect.center = ((display_width/2),(display_height/2))
                gameDisplay.blit(TextSurf, TextRect)
            elif user2.properties['status'] ==3:
                text = user2.properties['name']+" Win!"
                largeText = pygame.font.Font('HUDaku.ttf',115)
                TextSurf, TextRect = text_objects(text, largeText)
                TextRect.center = ((display_width/2),(display_height/2))
                gameDisplay.blit(TextSurf, TextRect)
            if(user1.properties['status'] in attacks)and(user2.properties['status'] in attacks):
                if user1.properties['status'] < user2.properties['status']:
                    text = user2.properties['name']+" Win!"
                    largeText = pygame.font.Font('HUDaku.ttf',115)
                    TextSurf, TextRect = text_objects(text, largeText)
                    TextRect.center = ((display_width/2),(display_height/2))
                    gameDisplay.blit(TextSurf, TextRect)
                elif user1.properties['status'] > user2.properties['status']:
                    text = user1.properties['name']+" Win!"
                    largeText = pygame.font.Font('HUDaku.ttf',115)
                    TextSurf, TextRect = text_objects(text, largeText)
                    TextRect.center = ((display_width/2),(display_height/2))
                    gameDisplay.blit(TextSurf, TextRect)
                else :
                    pass
            if (user1.properties['status'] ==0 and (user2.properties['status'] in attacks))|((user1.properties['status'] in attacks) and user2.properties['status']==0):
                if user1.properties['status'] ==0:
                    text = user2.properties['name']+" Win!"
                    largeText = pygame.font.Font('HUDaku.ttf',115)
                    TextSurf, TextRect = text_objects(text, largeText)
                    TextRect.center = ((display_width/2),(display_height/2))
                    gameDisplay.blit(TextSurf, TextRect)
                else:
                    text = user1.properties['name']+" Win!"
                    largeText = pygame.font.Font('HUDaku.ttf',115)
                    TextSurf, TextRect = text_objects(text, largeText)
                    TextRect.center = ((display_width/2),(display_height/2))
                    gameDisplay.blit(TextSurf, TextRect)
class User1:
    attacks = [1,2,3];
    properties = {"name":"근화","status":0,"energy":0}
    old_properties = {"name":"KKH","status":0,"energy":0}
    # -1 :막기
    # 0 : 으
    # 1 : 파
    # 2 : 에너지파 3>>1 그러나,막기로 막을 수 있음
    # 3 : 원기옥 
    # 기 상태
    strategy = [0,-1,1,0,0,2,0,0,0,3,0,0];
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
            self.display_status(self.properties['status']);
        except:
            print(self.properties['name']+"Lose!");
            sys.exit();
    def setOther(self,other):
        self.otherProperties = other.old_properties
    def afterTurn(self):
        for i in self.old_properties:
            self.old_properties[i] = self.properties[i];
    def display_status(self,status):
        global user1_image;
        if status == 0:
            user1_image = pygame.image.load("user1_0.jpg")
        elif status ==1:
            user1_image = pygame.image.load("user1_1.jpg")
        elif status ==-1:
            user1_image = pygame.image.load("user1_-1.jpg")
        elif status ==2:
            user1_image = pygame.image.load("user1_2.jpg")
        else:
            user1_image = pygame.image.load("user1_3.jpg")
        user1_image = pygame.transform.scale(user1_image, (200, 250))
    def show_status(self):
        status =  self.properties['status']
        if status == 0:
            return "으~"
        elif status == -1:
            return "막기"
        elif status == 1:
            return "파!"
        elif status == 2:
            return "에너지파!"
        else:
            return "원기옥!"
        
    def show_energy(self):
        return str(self.properties['energy'])
class User2:
    attacks = [1,2,3];
    properties = {"name":"현석","status":0,"energy":0}
    old_properties = {"name":"SHS","status":0,"energy":0}
    # -1 :막기
    # 0 : 으
    # 1 : 파
    # 2 : 에너지파 3>>1 그러나,막기로 막을 수 있음
    # 3 : 원기옥 
    # 기 상태
    strategy = [0,-1,1,0,0,2,0,0,0,3,0,1];
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
            self.display_status(self.properties['status']);
        except:
            print(self.properties['name']+"Lose!");
            sys.exit();
    def setOther(self,other):
        self.otherProperties = other.old_properties
    def afterTurn(self):
        for i in self.old_properties:
            self.old_properties[i] = self.properties[i];
    def display_status(self,status):
        global user2_image;
        if status == 0:
            user2_image = pygame.image.load("user1_0.jpg")
            
        elif status ==1:
            user2_image = pygame.image.load("user1_1.jpg")
        elif status ==-1:
            user2_image = pygame.image.load("user1_-1.jpg")
        elif status ==2:
            user2_image = pygame.image.load("user1_2.jpg")
        else:
            user2_image = pygame.image.load("user1_3.jpg")
        user2_image = pygame.transform.flip(user1_image, 1, 0)
        user2_image = pygame.transform.scale(user2_image, (200, 250))
    def show_status(self):
        status =  self.properties['status']
        if status == 0:
            return "으~"
        elif status == -1:
            return "막기"
        elif status == 1:
            return "파!"
        elif status == 2:
            return "에너지파!"
        else:
            return "원기옥"
    def show_energy(self):
        return str(self.properties['energy'])
    

user1 = User1();
user2 = User2();
user1.setOther(user2);
user2.setOther(user1);
    
carImg = pygame.image.load('user1_0.jpg')
carImg = pygame.transform.scale(carImg, (200, 100)) 
 
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos();
                condition = [150,450,100,50];
                if condition[0]+condition[2] > mouse[0] > condition[0] and condition[1]+condition[3] > mouse[1] > condition[1]:
                    global i;
                    i+=1;
                    print(i);
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_main();
                    i+=1;
                    
        gameDisplay.fill(white)
        display()
        pygame.display.update()
        clock.tick(15)
def game_main():
    global i;
    global isFinished;
    attacks = [1,2,3];
    print("Turn"+str((i+1)))
    user1.next_step(i);
    user2.next_step(i);
    print(user1.properties['name']+' : '+user1.show_status()+' VS '+user2.properties['name']+' : '+user2.show_status());
    print("Energy : "+user1.properties['name']+' = '+user1.show_energy()+' VS '+user2.properties['name']+' = '+user2.show_energy());
    if user1.properties['status'] !=user2.properties['status']:
        if user1.properties['status'] == 3:
            isFinished =True;
        elif user2.properties['status'] ==3:
            isFinished =True;
        if(user1.properties['status'] in attacks)and(user2.properties['status'] in attacks):
            if user1.properties['status'] < user2.properties['status']:
                isFinished =True;
            elif user1.properties['status'] > user2.properties['status']:
                isFinished =True;
            else :
                pass
        if (user1.properties['status'] ==0 and (user2.properties['status'] in attacks))|((user1.properties['status'] in attacks) and user2.properties['status']==0):
            if user1.properties['status'] ==0:
                isFinished =True;
            else:
                isFinished =True;
    user1.afterTurn();
    user2.afterTurn();

game_intro()
pygame.quit()
quit()