import http.client

host = "127.0.0.1:8080"
conn = http.client.HTTPConnection(host)
conn.request("GET", "/score")
conn.send(bytes("robtest1".encode()))
response = conn.getresponse()
print(response.status, response.readline())