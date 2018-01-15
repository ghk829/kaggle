import pygame
import time
import random
import sys

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