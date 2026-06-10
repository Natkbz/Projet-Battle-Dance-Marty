import http.client

conn = http.client.HTTPConnection("192.168.118.1", 8080)

conn.request("POST", "/step", body="robtest1 G ALU+ARU XNT")

response = conn.getresponse()

print(response.status)
print(response.read().decode())