import time

from martypy import Marty
from robot.MartyColor import MartyColor
import threading

class MartyContext():
    def __init__(self, addressIP):
        self.addressIP = addressIP
        self.marty = None
        self.martyColor = None

    def connect(self):
        try:
            self.marty = Marty("wifi", self.addressIP)
            if self.marty.is_conn_ready():
                self.marty.stand_straight(500)
                self.martyColor = MartyColor(self.marty)
                print("connexion réussi")
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la connexion à {self.addressIP} : {e}")
            return False
        
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
        angleLow = -45
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
    
    def eyes_expression(self,emotion,blocking):
        valid_emotion = { "angry", "excited", "normal", "wide", "wiggle"}
        if emotion in valid_emotion:
            self.marty.eyes(emotion,1000,blocking)
        else : 
            print ("Emotion is not valid")
    
    def expression(self,expr):
        valid_expression={"XNT","XSD","XNG","XHP","XND"}
        if expr in valid_expression:
            match expr:
                case "XNT":
                    self.normal(1500)
                    self.eyes_expression("normal",False)
                    self.marty.hold_position(3000,True)
                case "XSD":
                    self.normal(1500)
                    self.eyes_expression("wide",False)
                    self.marty.disco_color("Blue")
                    self.marty.hold_position(3000,True)
                case "XNG":
                    self.normal(1500)
                    self.eyes_expression("angry",False)
                    self.marty.disco_color("Red")
                    self.marty.hold_position(3000,True)
                case "XHP":
                    self.eyes_expression("normal",False)
                    self.marty.disco_color("Green")
                    self.dance()
                case "XND":
                    def rainbow_eyes():
                        colors = [(255, 0, 0),(255, 127, 0),(255, 255, 0),(0, 255, 0),(0, 0, 255),(75, 0, 130),(148, 0, 211)]
                        for i in range(2):
                            self.eyes_expression("wiggle",False)
                            for color in colors:
                                self.marty.disco_color(color)
                                time.sleep(0.25)
                    arc_en_ciel_thread = threading.Thread(target=rainbow_eyes)
                    arc_en_ciel_thread.start()
                    self.dance()
            self.marty.disco_color("None")
            self.normal(1500)
        else:
            print(f"Expression {expr} non valide ")
        
    def dance(self):
        #block 1
        self.marty.move_joint('left arm', 75, 800,False)
        self.marty.move_joint('right arm', 75,800,False)
        self.marty.move_joint('left knee', 20, 800,False)
        self.marty.move_joint('right knee', 20,800)
        #block 2
        self.marty.move_joint('left arm', -45, 800,False)
        self.marty.move_joint('right arm', 130, 800,False)
        self.marty.move_joint('left knee', -20, 800,False)
        self.marty.move_joint('right knee', -20, 800)
        #block 3
        self.marty.move_joint('left arm', 130, 800,False)
        self.marty.move_joint('right arm', -45, 800,False)
        self.marty.move_joint('left knee', 20, 800,False)
        self.marty.move_joint('right knee', 20, 800)
        
        
        
        
    def normal(self,duration):
        return self.marty.stand_straight(duration)
    def getBattery(self):
        return self.marty.get_battery_remaining()
    
    def getColor(self):
        return self.martyColor.detectColor()
    
    def CalibrateColor(self):
        self.martyColor.lunchFullCalibration()        