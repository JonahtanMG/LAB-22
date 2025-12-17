import requests
r = requests.get("https://httpbin.org/get")
respuesta = r.json()

print("IP:", respuesta["IP"])
print("Headers:", respuesta["headers"])
print("Args:", respuesta["args"])