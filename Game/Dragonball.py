import sys;
import time;
import matplotlib.image as mpimg
import matplotlib.pyplot as plt;
import numpy as np;
class User1:
    attacks = [1,2,3];
    properties = {"name":"근화","status":0,"energy":0}
    old_properties = {"name":"KKH","status":0,"energy":0}
    probabilities = {-1:0.2,0:0.2,1:0.2,2:0.2,3:0.2};
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
        global i;
        if self.otherProperties['energy'] == 0:
              self.probabilities[0] = 1;
              for key in self.probabilities.keys():
                  if key != 0:
                      self.probabilities[key] = 0;
        if self.properties['energy'] == 1:
            self.probabilities[2] = 0;
            self.probabilities[3] = 0;
            l = 0
            for key in self.probabilities:
                if self.probabilities[key] != 0:
                    l+=1;
            prob = 1.0/l
            for key in self.probabilities:
                if self.probabilities[key] != 0:
                    self.probabilities[key] = prob;
        if self.properties['energy'] == 2:
            self.probabilities[3] = 0;
            l = 0
            for key in self.probabilities:
                if self.probabilities[key] != 0:
                    l+=1;
            prob = 1.0/l
            for key in self.probabilities:
                if self.probabilities[key] != 0:
                    self.probabilities[key] = prob;
        if self.properties['energy'] == 3:
             self.probabilities[3] = 1;
             for key in self.probabilities.keys():
                 if key != 3:
                     self.probabilities[key] = 0;
        sample_choice = np.random.choice(list(self.probabilities.keys()),p=list(self.probabilities.values()));
        flag = False;
        for key in self.probabilities:
            if self.probabilities[key] == 1.0:
                flag = True;
                break;
        if flag:
            for key in self.probabilities:
                self.probabilities[key] =0.2;
        if (i+1) > len(self.strategy):
            self.strategy.append(sample_choice);
        else:
            self.strategy[i] = sample_choice;
        
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
    strategy = [0,0,0,3,0,1,0];
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
        
if __name__ == "__main__":
    user1 = User1();
    user2 = User2();
    user1.setOther(user2);
    user2.setOther(user1);
    
    # main
    flag = True;
    attacks = [1,2,3];
    i = 0;
    plt.ion();
    while(flag):
        print("Turn"+str((i+1)))
        user1.next_step(i);
        user2.next_step(i);
        print(user1.properties['name']+' : '+user1.show_status()+' VS '+user2.properties['name']+' : '+user2.show_status());
        print("Energy : "+user1.properties['name']+' = '+user1.show_energy()+' VS '+user2.properties['name']+' = '+user2.show_energy());
        if user1.properties['status'] !=user2.properties['status']:
            if user1.properties['status'] == 3:
                print(user1.properties['name']+" Win!");
                break;
            elif user2.properties['status'] ==3:
                print(user2.properties['name']+" Win!")
                break;
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
        i+=1;