import http.client

class Client():
    
    ip = 0
    port = 0
    conn = 0
    
    def __init__(self, ip_connection, port_connection):
        self.port = port_connection
        self.ip = ip_connection
        self.conn = http.client.HTTPConnection(self.ip, self.port)
        
        
    def testConnection(self):
        self.conn.request("GET", "/")
        
        response = self.conn.getresponse()
        
        rep = response.read().decode()
        print(response.status)
        print(rep)
        
        return rep
    
    
    def getId(self):
        self.conn.request("POST", "/hello")
        
        response = self.conn.getresponse()
        
        print(response.status)
        id = response.read().decode()
        print(id)
        
        return id
    
    
    def getScore(self, id):
        self.conn.request("GET", "/score", body=id)
        
        response = self.conn.getresponse()

        score = response.read().decode()
        print(response.status)
        print(score)
        
        return score
    
    
    def start(self, id):
        self.conn.request("POST", "/start", body=id)
        
        response = self.conn.getresponse()
        
        nbrPas = response.read().decode()
        print(response.status)
        print(nbrPas)
        
        return nbrPas
        
    
    def deconnecter(self, id):
        self.conn.request("POST", "/bye", body=id)
        
        response = self.conn.getresponse()
        
        rep = response.read().decode()
        print(response.status)
        print(rep)
        
        return rep
    
    
    def sendStep(self, id, col, arm, exp):
        self.conn.request("POST", "/step", body=f"{id} {col} {arm} {exp}")

        response = self.conn.getresponse()

        point = response.read().decode()
        print(response.status)
        print(point)
        
        return point
    
    
    
    
    
# ###############TESTS###################    
# client = Client("10.169.196.150", 8080)
# id1 = client.getId()
# print(client.start(id1))
# print(client.getScore(id1))
# print(f"points du step : {client.sendStep(id1, "N", "ALB", "XSD")}")
# print(client.getScore(id1))
# print(client.deconnecter(id1))
# print(f"Mon id unique est : {id1}")
# client2 = Client("127.0.0.1", 8080)
# id2 = client2.getId()
# print(f"Le miens est : {id2}")
# # #######################################
        
    
    