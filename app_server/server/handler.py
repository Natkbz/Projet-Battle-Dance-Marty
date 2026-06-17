import http.server
import random
import json
from server.robot import Robot


class Handler(http.server.BaseHTTPRequestHandler):
    def send_json(self, code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw)

    def do_GET(self):
        if self.path == "/":
            self.send_json(200, {"version": self.server_version})

        elif self.path == "/score":
            try:
                data = self.read_json()
                robot_id = data["robot_id"]           # KeyError si absent

                robot = self.server.serv_instance.recherche_robot(robot_id)

                signaux = self.server.serv_instance.signaux
                signaux.requete_recue.emit(
                    f"GET /score : Demande de score par {robot_id}"
                )

                self.send_json(200, {"score": robot.getScore_final()})

            except KeyError:
                self.send_json(400, {"error": "Champ 'robot_id' manquant"})
            except Exception:
                self.send_json(404, {"error": "Robot non trouvé"})

    def do_POST(self):
        if self.path == "/hello":
            new_robot = Robot()
            new_id = str(random.randint(0, 9999999))
            new_robot.setId(new_id)

            self.server.serv_instance.ajouter_robot(new_robot)

            signaux = self.server.serv_instance.signaux
            signaux.requete_recue.emit(
                f"POST /hello : Nouveau robot connecté (ID: {new_id})"
            )
            signaux.robot_ajoute.emit(new_id)

            self.send_json(200, {"id": new_id})

        elif self.path == "/start":
            try:
                data = self.read_json()
                robot_id = data["robot_id"]

                signaux = self.server.serv_instance.signaux
                signaux.requete_recue.emit(
                    f"POST /start : Début de la battle pour {robot_id}"
                )

                robot = self.server.serv_instance.recherche_robot(robot_id)
                nombre_de_pas = int(
                    self.server.serv_instance.getNombreDePasBattle()
                )
                robot.setNbrDePasRestants(nombre_de_pas)
                robot.setScore(0)
                #on charge les regles actuelles
                regles_serveur = self.server.serv_instance.regles_points
                robot.setRegles(regles_serveur)
                
                signaux.pas_mis_a_jour.emit(robot_id, nombre_de_pas)
                self.send_json(200, {"nombre_de_pas": nombre_de_pas})

            except KeyError:
                self.send_json(400, {"error": "Champ 'robot_id' manquant"})
            except Exception:
                self.send_json(404, {"error": "Robot non trouvé"})

        elif self.path == "/bye":
            try:
                data = self.read_json()
                robot_id = data["robot_id"]

                self.server.serv_instance.supprimer_robot(robot_id)

                signaux = self.server.serv_instance.signaux
                signaux.requete_recue.emit(
                    f"POST /bye : Déconnexion du robot {robot_id}"
                )
                signaux.robot_supprime.emit(robot_id)

                self.send_json(200, {"status": "OK"})

            except KeyError:
                self.send_json(400, {"error": "Champ 'robot_id' manquant"})

        elif self.path == "/step":
            try:
                data = self.read_json()
                robot_id = data["robot_id"]
                col = data["col"]
                arm = data["arm"]
                exp = data["exp"]

                

                robot = self.server.serv_instance.recherche_robot(robot_id)

                if robot.getNbrDePasRestants() <= 0:
                    signaux = self.server.serv_instance.signaux
                    signaux.requete_recue.emit(
                        f"POST /step : Rejeté, le robot {robot_id} n'a plus de pas"
                    )
                    self.send_json(403, {"error": "Plus de pas restants pour ce robot"})
                    return 
                point = self.server.serv_instance.calculPoint(col, arm, exp,robot.getRegles())
                robot.addToScore_final(int(point))
                robot.decreaseNbrDePasRestants()
                
                signaux = self.server.serv_instance.signaux
                signaux.requete_recue.emit(
                    f"POST /step : Le robot {robot_id} gagne {point} pts"
                )
                signaux.score_mis_a_jour.emit(robot_id, robot.getScore_final())
                signaux.pas_mis_a_jour.emit(robot_id, robot.getNbrDePasRestants())

                self.send_json(200, {"points": int(point)})

            except KeyError:
                self.send_json(
                    400,
                    {"error": "Champs manquants (robot_id, col, arm, exp)"},
                )
            except Exception as e:
                self.send_json(500, {"error": f"Crash interne : {str(e)}"})