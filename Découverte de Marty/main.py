from martypy import Marty
import time

from MartyContext import MartyContext

def main():
    ip_robot = "192.168.0.109"  

    mon_marty = MartyContext(ip_robot)


    mon_marty.move_foot('U', 3)
    

# Point d'entrée du script
if __name__ == "__main__":
    main()

""""
def move_arm(marty,type):
    if(type == 'ALU'):
        marty.move_joint('left arm', 140, 1000)
    
    
def getColor(marty):
    colorR = marty.get_color_sensor_value_by_channel('left','red')
    colorG = marty.get_color_sensor_value_by_channel('left','green')
    colorB = marty.get_color_sensor_value_by_channel('left','blue')
    return (colorR,colorG,colorB)

def calibrageCouleur(marty,couleur):
    print("placer la couleur ",couleur,"sous le marty")
    input("Appuyez sur Entrée quand le pied est bien positionné...")
    valeurR =[]
    valeurG = []
    valeurB = []
    for i in range(10) :
        color = getColor(marty)
        valeurR.append(color[0])
        valeurG.append(color[1])
        valeurB.append(color[2])
        time.sleep(1)
    moyenneR = sum(valeurR)/10
    moyenneG = sum(valeurG)/10
    moyenneB = sum(valeurB)/10
    print("calibrage finit")
    return (moyenneR,moyenneG,moyenneB)

def calibrageTotal(marty):
    jaune = calibrageCouleur(marty,"jaune")
    rose = calibrageCouleur(marty,"rose")
    noir = calibrageCouleur(marty,"noir")
    vert = calibrageCouleur(marty,"vert")
    

my_marty = connect("192.168.0.109")
my_marty.stand_straight(500)
#print(have_walk)
#move_foot(my_marty,'U',3)
#move_foot(my_marty,'L',1)
#move_foot(my_marty,'B',2)
#move_arm(my_marty,'ALU')
jaune = calibrageCouleur(my_marty,"jaune")
rose = calibrageCouleur(my_marty,"rose")
noir = calibrageCouleur(my_marty,"noir")
vert = calibrageCouleur(my_marty,"vert")
print("jaune", jaune)
print("rose",rose)
print("noir",noir)
print("vert",vert)
"""
