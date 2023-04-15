import json
import requests

allPokemonBasicData = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0").json()

print(allPokemonBasicData)
