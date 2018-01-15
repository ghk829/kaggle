class User1:
    attacks = [1,2,3];
    properties = {"name":"병화","status":0,"energy":0}
    old_properties = {"name":"KKH","status":0,"energy":0}
    # -1 :막기
    # 0 : 으
    # 1 : 파
    # 2 : 에너지파 3>>1 그러나,막기로 막을 수 있음
    # 3 : 원기옥 
    # 기 상태
    strategy = [];
    def __init__(self):
        pass
    def next_step(self,step):
        # 정의해야 할 Method
        # 아래 코드는 건들지 말 것
        if user1.properties['energy'] == 0
            self.step = 0
        elif user1.properties['energy'] > user2.properties['energy']:
            self.step = 0
        elif user1.properties['energy'] == user2.properties['energy']:
            self.step = 1
        else :
            self.step = -1
        self.strategy.append[self.step]
            
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
            return "원기옥"
        
    def show_energy(self):
        return str(self.properties['energy'])
