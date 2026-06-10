import http.server
import random
from server.robot import Robot

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

            try:
                self.server.serv_instance.recherche_robot(robot_id)
                
                #envoie d'un signal pour ajouter un log
                signaux = self.server.serv_instance.signaux
                signaux.requete_recue.emit(f"GET /score : Demande de score par {robot_id}")
                
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                
                self.wfile.write(bytes(str(self.server.serv_instance.recherche_robot(robot_id).getScore_final()).encode()))
                print(self.server.serv_instance.recherche_robot(robot_id).getScore_final())
                
            except Exception as e:
                self.send_response(404)
                self.send_header("Content-type", "text")
                self.end_headers()
                
                self.wfile.write(bytes("Robot not found".encode()))

    def do_POST(self):
        request = self.requestline
        list = request.split(" ")
        
        if(list[1] == "/hello"):
            newRobot = Robot()
            newId = (str(random.randint(0,9999999)))
            newRobot.setId(newId)
            
            self.server.serv_instance.ajouter_robot(newRobot)
            #envoie du signal dans la console et pour dire qu'un robot a été ajouté
            signaux = self.server.serv_instance.signaux
            signaux.requete_recue.emit(f"POST /hello : Nouveau robot connecté (ID: {newId})")
            signaux.robot_ajoute.emit(newId)
            
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            
            self.wfile.write(bytes(newId.encode()))
            
        elif(list[1] == "/start"):
            length = int(self.headers['Content-Length'])
            robot_id = self.rfile.read(length).decode()
            
            #signal pour dire qu'un robot commence sa battle
            signaux = self.server.serv_instance.signaux
            signaux.requete_recue.emit(f"POST /start : Début de la battle pour {robot_id}")
            
            print(robot_id)
            
            try:
                self.server.serv_instance.recherche_robot(robot_id).setNbrDePasRestants(int(self.server.serv_instance.getNombreDePasBattle()))
                self.server.serv_instance.recherche_robot(robot_id).setScore(0)
                
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                
                self.wfile.write(bytes(self.server.serv_instance.getNombreDePasBattle().encode()))
            
            except Exception as e:
                self.send_response(404)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write(bytes("Robot not found".encode()))
            
            
            
            
            
        elif(list[1] == "/bye"):
            length = int(self.headers['Content-Length'])
            robot_id = self.rfile.read(length).decode()
            
            self.server.serv_instance.supprimer_robot(robot_id)
            
            #envoie de signal pour dire qu'un robot s'est déco à la console et à la liste de robot
            signaux = self.server.serv_instance.signaux
            signaux.requete_recue.emit(f"POST /bye : Déconnexion du robot {robot_id}")
            signaux.robot_supprime.emit(robot_id)
            
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
            
            try:
                robot = self.server.serv_instance.recherche_robot(robot_id)
            
                if(robot.getNbrDePasRestants() <= 0):
                    point = "0"
                
                robot.addToScore_final(int(point))
                robot.decreaseNbrDePasRestants()
                
                #envoie de signaux pour dire qu'un nouveau score a été calculé à la console et au score ds le tableau
                signaux = self.server.serv_instance.signaux
                signaux.requete_recue.emit(f"POST /step : Le robot {robot_id} gagne {point} pts")
                signaux.score_mis_a_jour.emit(robot_id, robot.getScore_final())
                
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                
                self.wfile.write(bytes(point.encode()))
                
            except Exception as e:
                self.send_response(404)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write(bytes("Robot non trouvé ou plus de pas restants".encode()))
            
            
            
            