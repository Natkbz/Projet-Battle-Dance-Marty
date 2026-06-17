import http.client
import json


class Client():

    ip = 0
    port = 0
    conn = 0

    def __init__(self, ip_connection, port_connection):
        self.port = port_connection
        self.ip = ip_connection
        self.conn = http.client.HTTPConnection(self.ip, self.port)



    def request_json(self, method, path, data = None):
        if (data != None):
            body = json.dumps(data).encode("utf-8")
            headers = {"Content-Type": "application/json"}
            self.conn.request(method, path, body=body, headers=headers)
        else:
            self.conn.request(method, path)

        response = self.conn.getresponse()
        raw = response.read().decode("utf-8")

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {}

        print(f"{method} {path} : {response.status}(code), result : {parsed}")
        return response.status, parsed


    def testConnection(self):
        status, data = self.request_json("GET", "/")
        return data.get("version", "")

    def getId(self):
        status, data = self.request_json("POST", "/hello")
        return data.get("rid", "")

    def getScore(self, id):
        status, data = self.request_json("GET", "/score", {"robot_id": id})
        return data.get("score")

    def start(self, id):
        status, data = self.request_json("POST", "/start", {"robot_id": id})
        return data.get("steps")

    def deconnecter(self, id):
        status, data = self.request_json("POST", "/bye", {"robot_id": id})
        return data.get("status", "")

    def sendStep(self, id, col, arm, exp):
        status, data = self.request_json(
            "POST", "/step",
            {"rid": id, "col": col, "arm": arm, "exp": exp}
        )
        return data.get("points")


# ###############TESTS###################
# client = Client("169.254.102.198", 8080)
# id1 = client.getId()
# print(client.start(id1))
# print(client.getScore(id1))
# print(f"points du step total du step : {client.sendStep(id1, 'N', 'ALB', 'XSD')}")
# print(f"points du step total du step : {client.sendStep(id1, 'N', 'ALB', 'XSD')}")
# print(client.getScore(id1))
# print(client.deconnecter(id1))
# print(f"Mon id unique est : {id1}")
# client2 = Client("127.0.0.1", 8080)
# id2 = client2.getId()
# print(f"Le miens est : {id2}")
# #######################################