class User1:
    attacks = [1,2,3];
    properties = {"name":"KKH","status":0,"energy":0}
    old_properties = {"name":"KKH","status":0,"energy":0}
    # -1 :막기
    # 0 : 으
    # 1 : 파
    # 3 : 에너지파 3>>1 그러나,막기로 막을 수 있음
    # 5 : 원기옥 
    # 기 상태
    strategy = [0,0,1,0,0,0,0,0];
    def __init__(self):
        pass
    def next_step(self,step):
        # 정의해야 할 Method
        self.properties['status'] = self.strategy[step]
        if self.properties['status'] == 0:
            self.properties['energy']+=1;
        elif self.properties['status'] in self.attacks:
            if self.properties['energy'] < self.properties['status']:
                self.properties['status'] = 0;
                self.properties['energy']+=1;
            else:
                self.properties['energy']-=self.properties['status'];
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
    # 3 : 에너지파 3>>1 그러나,막기로 막을 수 있음
    # 5 : 원기옥 
    # 기 상태
    strategy = [0,0,0,3,0,0,0,0];
    def __init__(self):
        pass
    def next_step(self,step):
        # 정의해야 할 Method
        self.properties['status'] = self.strategy[step]
        if self.properties['status'] == 0:
            self.properties['energy']+=1;
        elif self.properties['status'] in self.attacks:
            if self.properties['energy'] < self.properties['status']:
                self.properties['status'] = 0;
                self.properties['energy']+=1;
            else:
                self.properties['energy']-=self.properties['status'];
    def setOther(self,other):
        self.otherProperties = other.old_properties
    def afterTurn(self):
        for i in self.old_properties:
            self.old_properties[i] = self.properties[i];
        
user1 = User1();
user2 = User2();
user1.setOther(user2);
user2.setOther(user1);

# main
attacks = [1,2,3];
for i in range(10):
    user1.next_step(i);
    user2.next_step(i);
    if user1.properties['status'] !=user2.properties['status']:
        if user1.properties['status'] == 3:
            print(user1.properties['name']+" Win!");
        elif user2.properties['status'] ==3:
            print(user2.properties['name']+" Win!")
            
        if(user1.properties['status'] in attacks)and(user2.properties['status'] in attacks):
            if user1.properties['status'] < user2.properties['status']:
                print(user2.properties['name']+" Win!");
                break;
            elif user1.properties['status'] > user2.properties['status']:
                print(user1.properties['name']+" Win!")
                break;
            else :
                pass
        if (user1.properties['status'] ==0 and (user2.properties['status'] in attacks))|((user1.properties['status'] in attacks) and user2.properties['status']==0):
            if user1.properties['status'] ==0:
                print(user2.properties['name']+" Win!")
                break;
            else:
                print(user1.properties['name']+" Win!")
                break;
    user1.afterTurn();
    user2.afterTurn();