from dance.FileDance import FileDance
from robot.MartyContext import MartyContext
class MartyDance:
    def __init__(self,path,marty_):
        self.marty = marty_
        self.file_dance = FileDance(path)
        self.move = self.file_dance.getMvt()
        self.colorDance = self.file_dance.getColorDance()
        print(self.move)
        print(self.colorDance)

    def dance(self):
        for i in range(6):
            print("mouvement ",i)
            self.execute_mouvement(i)
            self.marty.normal(1500)
            self.check_color()
            
            
    def execute_mouvement(self,n_move):
        self.marty.move_foot(self.move[n_move][0], int(self.move[n_move][1]))
        
    def check_color(self):
        color = self.marty.getColor()
        print(color)
        if color in self.colorDance:
            bras = self.colorDance[color][0]
            expressionToDo = self.colorDance[color][1]
            for i in range(len(bras)):
                self.marty.move_arm(bras[i])
            self.marty.expression(expressionToDo)
