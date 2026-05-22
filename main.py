import http.server

PORT = 8000

nombreDePasBattle = 10    ########TEMPORAIRE#########

def recherche_robot(id):
    for i in range(len(liste_robots)):
        if(liste_robots[i].id == id):
            return liste_robots[i]


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
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            idRequeset = self.rfile.readline()
            self.wfile.write(bytes(recherche_robot(idRequeset).score_final))
            
            
    def do_POST(self):
        request = self.requestline
        list = request.split(" ")
        
        if(list[1] == "/hello"):
            newRobot = Robot()
            newId = ("bot" + len(liste_robots))
            newRobot.setId(newId)
            
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
            
            
            
            

server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)


liste_robots = []
robot_1 = Robot()
liste_robots.append(robot_1)


def run() :
    print("serving at port", PORT)
    server.serve_forever()

run()