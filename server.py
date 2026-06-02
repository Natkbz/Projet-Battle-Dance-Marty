import http.server
import random

PORT = 8080

nombreDePasBattle = "10"    ########TEMPORAIRE#########

liste_robots = []

countRobots = 0


def recherche_robot(id):
    for i in range(len(liste_robots)):
        if(liste_robots[i].id == id):
            return liste_robots[i]
        
def supprimer_robot(id):
    for i in range(len(liste_robots)):
        if(liste_robots[i].id == id):
            liste_robots.pop(i)
            
def calculPoint(col, arm, exp):
    ##############TO DO : CALCULER LES POINTS
    
    return "0"

class Robot():
    score_final = 0
    id = 0
    nombreDePasRestants = 0
    
    def setId(self, id):
        self.id = id
    def setNbrDePasRestants(self, nbr):
        self.nombreDePasRestants = nbr



################### POUR LES TESTS ##################
robot_1 = Robot()
robot_1.setId("robtest1")
liste_robots.append(robot_1)
#####################################################


        
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        request = self.requestline
        list = request.split(" ")
        
        if (list[1] == "/"):
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes(self.server_version.encode()))
        elif(list[1] == "/score"):
            length = int(self.headers['Content-Length'])
            robot_id = self.rfile.read(length).decode()
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(str(recherche_robot(robot_id).score_final).encode()))              
            print(robot_1.score_final)
            
            
    def do_POST(self):
        request = self.requestline
        list = request.split(" ")
        
        if(list[1] == "/hello"):
            newRobot = Robot()
            newId = (str(random.randint(0,999999)))
            newRobot.setId(newId)
            
            #countRobots += 1
            liste_robots.append(newRobot)
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(newId.encode()))
            
        elif(list[1] == "/start"):
            length = int(self.headers['Content-Length'])
            robot_id = self.rfile.read(length).decode()
            print(robot_id)
            
            recherche_robot(robot_id).setNbrDePasRestants(int(nombreDePasBattle))
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(nombreDePasBattle.encode()))
            
        elif(list[1] == "/bye"):
            length = int(self.headers['Content-Length'])
            robot_id = self.rfile.read(length).decode()
            
            supprimer_robot(robot_id)
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes("OK".encode()))
            
            
        elif(list[1] == "/step"):
            length = int(self.headers['Content-Length'])
            string = self.rfile.read(length).decode()
            list_data = string.split(" ")
            
            robot_id = list_data[0]
            col = list_data[1]
            arm = list_data[2]
            exp = list_data[3]
            
            point = calculPoint(col, arm, exp)
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(point.encode()))
            
                  
server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)






def run() :
    print("serving at port", PORT)
    server.serve_forever()

run()