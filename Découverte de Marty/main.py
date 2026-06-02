from martypy import Marty
import time

from MartyContext import MartyContext

def main():
    ip_bot = "192.168.0.113" 

    my_marty = MartyContext(ip_bot)
    if(my_marty.connect()):
        print("Connexion réussi")
    else : 
        print("Connexion au Marty impossible")
        return 
    
    my_marty.CalibrateColor()
    print("color :",my_marty.getColor())
    
    
    

# Point d'entrée du script
if __name__ == "__main__":
    main()
