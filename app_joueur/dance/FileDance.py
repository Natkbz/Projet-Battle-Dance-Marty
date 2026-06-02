class FileDance:
    def __init__(self,path):
        self.file = open(path, 'r')
        self.movement = [] #format: [(dir1,step1),(dir2,step2)]
        self.colorDance = {} #format: {color1 : (bras,expr), color2 : (bras,expr)}
    
    def close(self):
        self.file.close()
    
    def readLine(self):
        line = self.file.readline()
        return line.rstrip("\n")