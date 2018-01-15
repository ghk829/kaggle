import pygame
import time
import random
import sys
class User1:
    attacks = [1,2,3];
    properties = {"name":"현석","status":0,"energy":0}
    old_properties = {"name":"SHS","status":0,"energy":0}
    probabilities = {-1:0.2,0:0.2,1:0.2,2:0.2,3:0.2};
    # -1 :막기
    # 0 : 으
    # 1 : 파
    # 2 : 에너지파 3>>1 그러나,막기로 막을 수 있음
    # 3 : 원기옥 
    # 기 상태
    strategy = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1];
    def __init__(self):
        pass
    def next_step(self,step):
            # 정의해야 할 Method
            if User2.properties['energy'] == 0:
                if self.properties['energy'] == 1:
                    self.strategy[step] = 1;
                self.strategy[step] = 0;
            elif User2.properties['energy'] == 1:
                if self.properties['energy'] == 2:
                    self.strategy[step] = 2;
                else:
                    self.strategy[step] = -1;
            elif User2.properties['energy'] == 2:
                self.strategy[step] = 0;
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