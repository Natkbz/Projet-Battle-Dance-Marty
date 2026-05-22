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
        
    def move_arm(self,type):
        time_moov = 500
        angleHigh = 130
        angleLow = 0
        if(type == 'ALU'):
            return self.marty.move_joint('left arm', angleHigh, time_moov)
        elif(type == 'ALB'):
            return self.marty.move_joint('left arm', angleLow, time_moov)
        elif(type == 'ARU'):
            return self.marty.move_joint('right arm', angleHigh, time_moov)
        elif(type == 'ARB'):
            return self.marty.move_joint('right arm', angleLow, time_moov)
        else : 
            return False
    
    def eyes_expression(self,emotion):
        valid_emotion = { "angry", "excited", "normal", "wide", "wiggle"}
        if emotion in valid_emotion:
            self.marty.eyes(emotion)
        else : 
            print ("Emotion is not valid")
        