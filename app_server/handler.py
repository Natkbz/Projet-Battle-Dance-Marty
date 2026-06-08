import http.server
import random
from robot import Robot

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
            
            self.wfile.write(bytes(str(self.server.serv_instance.recherche_robot(robot_id).getScore_final()).encode()))              
            print(self.server.serv_instance.recherche_robot(robot_id).getScore_final())
            
            
    def do_POST(self):
        request = self.requestline
        list = request.split(" ")
        
        if(list[1] == "/hello"):
            newRobot = Robot()
            newId = (str(random.randint(0,9999999)))
            newRobot.setId(newId)
            
            self.server.serv_instance.ajouter_robot(newRobot)
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(newId.encode()))
            
        elif(list[1] == "/start"):
            length = int(self.headers['Content-Length'])
            robot_id = self.rfile.read(length).decode()
            print(robot_id)
            
            self.server.serv_instance.recherche_robot(robot_id).setNbrDePasRestants(int(self.server.serv_instance.getNombreDePasBattle()))
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(self.server.serv_instance.getNombreDePasBattle().encode()))
            
        elif(list[1] == "/bye"):
            length = int(self.headers['Content-Length'])
            robot_id = self.rfile.read(length).decode()
            
            self.server.serv_instance.supprimer_robot(robot_id)
            
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
            
            point = self.server.serv_instance.calculPoint(col, arm, exp)
            self.server.serv_instance.recherche_robot(robot_id).addToScore_final(int(point))
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(point.encode()))