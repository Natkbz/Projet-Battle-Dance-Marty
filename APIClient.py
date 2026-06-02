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
        
        print(response.status)
        print(response.read().decode())
        
        return response.read().decode()
    
    
    def getId(self):
        self.conn.request("POST", "/hello")
        
        response = self.conn.getresponse()
        
        print(response.status)
        id = response.read().decode()
        print(id)
        
        return id
    
    

    
    
    
    
    
    
client = Client("127.0.0.1", 8080)
id1 = client.getId()
print(f"Mon id unique est : {id1}")
client2 = Client("127.0.0.1", 8080)
id2 = client2.getId()
print(f"Le miens est : {id2}")
        
        
    
    