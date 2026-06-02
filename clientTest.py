import http.client

conn = http.client.HTTPConnection("127.0.0.1", 8080)

conn.request("POST", "/bye", body="robtest1")

response = conn.getresponse()

print(response.status)
print(response.read().decode())