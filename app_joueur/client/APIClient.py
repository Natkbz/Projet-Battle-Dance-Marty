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
        version = data.get("version", "")
        if (version == "1.2"):
            return True
        else:
            return False 

    def getId(self):
        status, data = self.request_json("POST", "/hello")
        return data.get("rid", "")

    def getScore(self, id):
        status, data = self.request_json("GET", "/score", {"rid": id})
        return data.get("points")

    def start(self, id):
        status, data = self.request_json("POST", "/start", {"rid": id})
        return data.get("steps")

    def deconnecter(self, id):
        status, data = self.request_json("POST", "/bye", {"rid": id})
        return data.get("status", "")

    def sendStep(self, id, col, arm, exp):
        status, data = self.request_json(
            "POST", "/step",
            {"rid": id, "col": col, "arm": arm, "exp": exp}
        )
        return data.get("points")


