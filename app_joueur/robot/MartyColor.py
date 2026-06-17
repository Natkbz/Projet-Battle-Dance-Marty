from martypy import Marty
import time
import math
"""
Calibrage manuel 
jaune : (236,91,50)
vert : (43,37,28)
noir : (23,10,8)
mauve : (120,25,39)
bleu ciel: (66,63,80)
rouge : (106,17,21)
"""
class MartyColor():
    def __init__(self, marty_):
        self.marty = marty_
        self.colors = {"N":(29,12,10), "Y" : (304,119,62), "G" : (52,45,34), "R" : (138,24,26), "P" : (164,35,49), "C":(81,79,93), "B":(38,23,28)}
        self.full_name = {"N": "Noir", "Y": "Jaune", "G": "Vert", "R": "Rouge", "P":"Mauve", "C":"Bleu ciel", "B": "Bleu fonce"}
    
    def detectColor(self):
        current = self.getColorValue()
        colorCode = None
        min_distance = 5

        for code, ref in self.colors.items():
            distance = math.sqrt(
                (current[0] - ref[0])**2 + 
                (current[1] - ref[1])**2 + 
                (current[2] - ref[2])**2
            )
            
            if distance < min_distance:
                min_distance = distance
                colorCode = code
                
        return colorCode
    
    def getColorValue(self):
        colorR = self.marty.get_color_sensor_value_by_channel('left','red')
        colorG = self.marty.get_color_sensor_value_by_channel('left','green')
        colorB = self.marty.get_color_sensor_value_by_channel('left','blue')
        return (colorR,colorG,colorB)

    def calibrateOneCouleurValue(self,code):
        color = self.full_name.get(code, code)
        print("placer la couleur ",color,"sous le marty")
        input("Appuyez sur Entrée quand le pied est bien positionné...")
        valeurR =[]
        valeurG = []
        valeurB = []
        for i in range(10) :
            color = self.getColorValue()
            valeurR.append(color[0])
            valeurG.append(color[1])
            valeurB.append(color[2])
            time.sleep(0.1)
        meanR = sum(valeurR)/10
        meanG = sum(valeurG)/10
        meanB = sum(valeurB)/10
        print("calibrage finit ()",meanR," , ",meanG," , ",meanB)
        return (meanR,meanG,meanB)
    
    def captureColorValue(self, code):
        """Mesure et enregistre la couleur actuelle sous le robot (sans input, pour l'ui)."""
        valeurR = []
        valeurG = []
        valeurB = []
        for i in range(10):
            color = self.getColorValue()
            valeurR.append(color[0])
            valeurG.append(color[1])
            valeurB.append(color[2])
            time.sleep(0.1)
        meanR = sum(valeurR) / 10
        meanG = sum(valeurG) / 10
        meanB = sum(valeurB) / 10
        self.colors[code] = (meanR, meanG, meanB)
        return (meanR, meanG, meanB)
    
    def lunchFullCalibration(self):
        print("Début de la calibration complète...")
        for code in self.colors.keys():
            nouvelle_valeur = self.calibrateOneCouleurValue(code)
            self.colors[code] = nouvelle_valeur
        print("\n=== Toutes les couleurs ont été mises à jour avec succès ! ===")