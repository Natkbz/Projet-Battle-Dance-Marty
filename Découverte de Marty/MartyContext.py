from martypy import Marty

class MartyContext():
    def __init__(self,addressIp):
        self.marty = Marty("wifi",addressIp)
        self.marty.stand_straight(500)
        
    def move_foot(self,direction,nb_step):
        step_length = 30
        time_by_step = 1000
        if(direction == 'U'):
            return self.marty.walk(nb_step,'auto',0,step_length,time_by_step*nb_step)
        elif(direction == 'B'): 
            return self.marty.walk(nb_step,'auto',0,-step_length,time_by_step*nb_step)
        elif(direction == 'L'): 
            return self.marty.sidestep('left',nb_step,step_length,time_by_step*nb_step)
        elif(direction == 'R'): 
            return self.marty.sidestep('right',nb_step,step_length,time_by_step*nb_step)
        else :
            return False