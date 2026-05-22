from martypy import Marty
import time

from MartyContext import MartyContext

def main():
    ip_bot = "192.168.0.109"  

    #my_marty = MartyContext(ip_robot)
    my_marty = Marty("wifi",ip_bot)
    my_marty.stand_straight(500)
    print("jaune",calibrageCouleur(my_marty,"jaune"))
    
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
# Point d'entrée du script
if __name__ == "__main__":
    main()
