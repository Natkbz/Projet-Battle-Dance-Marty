from martypy import Marty


my_marty = Marty("wifi","192.168.0.101")
#marche en avant
#my_marty.walk(3,'auto',0,30,4000) 
#se remet droit normal
my_marty.stand_straight(1000)
#dance 
#my_marty.dance('right',  3000)
#yeux (emotion, temps de deplacement ms)
#my_marty.eyes('angry',1000) #froncé
#my_marty.eyes('normal',1000) #en haut
#my_marty.eyes('wide',1000) #ecarté 
#my_marty.eyes('wiggle',4000)#bouge partout
#coup de pied ( le pied, l'angle de la cheville, le temps)
#my_marty.kick('right',0,2000)
#les bras (angle bras gauche, angle bras droit, tmps dep)
#de -80 à 140 (-80 bras en arrière, 140 en haut et 0 en bas le long du corps)
#my_marty.arms(0,0,2000)
