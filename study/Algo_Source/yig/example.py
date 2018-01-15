class User2:
    attacks = [1,2,3];
    properties = {"name":"일근","status":0,"energy":0}
    old_properties = {"name":"YIG","status":0,"energy":0}
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
            self.probabilities[2] = 0.2;
            self.probabilities[3] = 0.2;
            l = 0
            for key in self.probabilities:
                if self.probabilities[key] != 0:
                    l+=1;
            prob = 1.0/l
            for key in self.probabilities:
                if self.probabilities[key] != 0:
                    self.probabilities[key] = prob;
        if self.properties['energy'] == 2:
            self.probabilities[3] = 0.2;
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
        
        if i == 0:
            self.strategy[i] = 0.0
        if i == 1:
            self.strategy[i] = -1.0          
        
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
