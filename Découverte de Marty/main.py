from martypy import Marty
import time

from MartyContext import MartyContext

def main():
    ip_bot = "192.168.0.109"  

    #my_marty = MartyContext(ip_robot)
    my_marty = Marty("wifi",ip_bot)
    my_marty.stand_straight(500)
    print("jaune",getColor(my_marty))
    
def getColor(marty):
    colorR = marty.get_color_sensor_value_by_channel('left','red')
    colorG = marty.get_color_sensor_value_by_channel('left','green')
    colorB = marty.get_color_sensor_value_by_channel('left','blue')
    return (colorR,colorG,colorB)


# Point d'entrée du script
if __name__ == "__main__":
    main()
