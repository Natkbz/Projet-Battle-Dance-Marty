import http.client

conn = http.client.HTTPConnection("127.0.0.1", 8080)

conn.request("POST", "/step", body="robtest1 G ALU+ARU XNT")

response = conn.getresponse()

print(response.status)
print(response.read().decode())