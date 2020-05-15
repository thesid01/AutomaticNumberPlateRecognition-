import os

class NumberPlates:
    def __init__(self):
        super().__init__()
        self.plates = []
        self.alphanum = []
    
    def readNumberPlates(self):
        for f in os.listdir('./NumberPlates'):
            if os.path.isfile(os.path.join('./NumberPlates', f)):
                self.plates.append(f)
    
    def readAlphaNum(self):
        for i in range(10):
            self.alphanum.append(str(i))
        for i in range(26):
            self.alphanum.append(chr(i+65))