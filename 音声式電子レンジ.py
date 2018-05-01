import re,socket

class World:
    def __init__(self):
        self.microwave = None
        self.s = None
        self.path = 'micro.txt'
        self.f = None
        
    def start(self):
        self.s = socket.socket()
        self.s.connect(('localhost', 10500))
        self.s.send(b'PAUSE\n')
        self.microwave = Abstractmicrowave(self)
        print("こんにちわ。")
        self.s.send(('RESUME\n').encode())
        self.microwave.search()
    
class Abstractmicrowave:
    def __init__(self,world):
        self.mode = None
        self.deg = []
        self.time = []
        self.order = ""
        self.auto = None
        self.stop = 0
        self.world = world
        self.sen = ""
        
    def search_time(self):
        if re.findall(r'[0-9]+\"+\"+分',self.order):
            self.time = re.findall(r'[0-9]+\"+\"+分',self.order)
            a = len(self.time)
            return a

        elif re.findall(r'[0-9]+\"+\"+秒',self.order):
            self.time = re.findall(r'[0-9]+\"+\"+秒',self.order)
            a = len(self.time)
            return a
        
        else:
            a = len(self.time)
            return a

    def search_deg(self):
        if re.findall(r'[0-9]+\"+\"+度',self.order):
            self.deg = re.findall(r'[0-9]+\"+\"+度',self.order)
            b = len(self.deg)
    
            return b

        else:
            b = len(self.deg)
            return b

    def search(self):
        while 1:
            data = world.s.recv(1024)
            a = data.decode('sjis')
            world.f = open(world.path, 'w')
            world.f.write(a)
            for line in open(world.path, 'r'):
                p = re.compile(r'<W.*?/>')
                if p.findall(line):
                    A = p.findall(line)
                    q = re.compile(r'\".*?\"')
                    if q.findall(A[0]):
                        self.sen = q.findall(A[0])
                        self.order = str(self.order) + str(self.sen[0])
            
            self.sen = ""
            self.order = str(self.order)
            print(self.order)
            mode_list = ["グリル","オーブン","レンジ","発酵"]
            for x in mode_list:
                if re.search(x,self.order):
                    self.mode = x
            self.T = self.search_time()
            self.D = self.search_deg()
            
            self.judgement()
            if self.stop == 1:
                break
            print("すみません。もう一度お願いします。")
        
        
    def searchA(self):
        auto_list = ["温め","解凍","牛乳","シフォンケーキ"]
        for x in auto_list:
            if re.search(x,self.order):
                self.auto = x

        self.read()

    def read(self):
        if self.auto == "温め":
            print("かしこまりました。温めを始めます。")
            self.stop = 1
    
            
        elif self.auto == "解凍":
            print("かしこまりました。解凍を始めます。")
            self.stop = 1
            
        elif self.auto == "牛乳":
            print("かしこまりました。牛乳を温めます。")
            self.stop = 1
    
            
        elif self.auto == "シフォンケーキ":
            print("かしこまりました。シフォンケーキを焼きます。")
            self.stop = 1
    
            
    def judgement(self):
        if self.T >= 1 and self.D >= 1: 
            print("かしこまりました。{}で{}で{}間焼きます。".format(self.mode,self.deg[0],self.time[0]))
            self.stop = 1

        elif self.T == 0 and self.D >= 1:
            print("{}で{}ですね。どのくらい焼きますか？".format(self.mode,self.deg[0]))
            self.order = ""
            self.search()
            
            
        elif self.T >= 1 and self.D == 0:
            print("{}で{}ですね。何度で焼きますか？".format(self.mode,self.time[0]))
            self.order = ""
            self.search()
            
            
        elif self.mode != None and self.T == 0 and self.D == 0:
            print("{}ですね。何度でどのくらい焼きますか？".format(self.mode))
            self.order = ""
            self.search()
            
            
            
        else:
            self.searchA()
    


world = World()
world.start()
