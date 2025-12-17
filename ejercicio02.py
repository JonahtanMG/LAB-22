import requests
r = requests.get("https://pokeapi.co/api/v2/pokemon")
pokemones = r.json()

for i in range(0, 10):
    print(i, ": ", pokemones["results"][i]["name"])