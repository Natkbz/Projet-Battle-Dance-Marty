import http.server

PORT = 8000

def recherche_robot(id):
    for i in range(len(liste_robots)):
        if(liste_robots[i].id == id):
            return liste_robots[i]


class Robot():
    score_final = 0
    id = 0
    def setId(self, id):
        self.id = id
        
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        request = self.requestline
        list = request.split(" ")
        
        if (list[1] == "/"):
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes(self.server_version))
        elif(list[1] == "/score"):
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(recherche_robot(list[2]).score_final))
            
            
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
            
            self.wfile.write(bytes(recherche_robot(list[2]).score_final))
            
            
            

server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)


liste_robots = []
robot_1 = Robot()
liste_robots.append(robot_1)


def run() :
    print("serving at port", PORT)
    server.serve_forever()

run()