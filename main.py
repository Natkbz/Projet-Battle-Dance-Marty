import http.server

PORT = 8080

nombreDePasBattle = 10    ########TEMPORAIRE#########

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

class Robot():
    score_final = 0
    id = 0
    nombreDePasRestants = 0
    
    def setId(self, id):
        self.id = id
    def setNbrDePasRestants(self, nbr):
        self.nombreDePasRestants = nbr
        
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
            idRequeset = self.rfile.readline()
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(recherche_robot(idRequeset).score_final))
            
            
    def do_POST(self):
        request = self.requestline
        list = request.split(" ")
        
        if(list[1] == "/hello"):
            newRobot = Robot()
            newId = ("bot" + countRobots)
            newRobot.setId(newId)
            
            countRobots += 1
            liste_robots.append(newRobot)
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(newId))
            
        elif(list[1] == "/start"):
            idRequeset = self.rfile.readline()
            
            recherche_robot(idRequeset).setNbrDePasRestants(nombreDePasBattle)
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(nombreDePasBattle))
            
        elif(list[1] == "/bye"):
            idRequeset = self.rfile.readline()
            
            supprimer_robot(idRequeset)
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes("OK".encode()))
            
            
            
                  
server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)


robot_1 = Robot()
liste_robots.append(robot_1)
robot_1.setId("robtest1")


def run() :
    print("serving at port", PORT)
    server.serve_forever()

run()