from martypy import Marty


def connect(addresse_ip) :
    marty = Marty("wifi",addresse_ip)
    marty.stand_straight(500)
    return marty

def move(marty,direction,nb_step):
    step_length = 30
    time_by_step = 1000
    if(direction == 'U'):
        marty.walk(nb_step,'auto',0,step_length,time_by_step*nb_step)
    elif(direction == 'B'): 
        marty.walk(nb_step,'auto',0,-step_length,time_by_step*nb_step)
    elif(direction == 'L'): 
        marty.sidestep('left',nb_step,step_length,time_by_step*nb_step)
    elif(direction == 'R'): 
        marty.sidestep('right',nb_step,step_length,time_by_step*nb_step)
    marty.stand_straight(500)


my_marty = connect("192.168.0.101")
move(my_marty,'U',3)
move(my_marty,'L',1)
move(my_marty,'B',2)
