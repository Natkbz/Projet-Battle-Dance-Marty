from martypy import Marty


my_marty = Marty("wifi","192.168.0.101")
#marche en avant
#my_marty.walk(3,'auto',0,30,4000) 
#se remet droit normal
my_marty.stand_straight(100)
#dance 
#my_marty.dance('right',  3000)
#yeux (emotion, temps de deplacement ms)
#my_marty.eyes('angry',1000) #froncé
#my_marty.eyes('normal',1000) #en haut
#my_marty.eyes('wide',1000) #ecarté 
#my_marty.eyes('wiggle',4000)#bouge partout