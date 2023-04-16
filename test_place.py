import requests

requestJson = requests.get(
    "https://raw.githubusercontent.com/arix2000/Pokedex_Data/develop/data/pokemon/pokemonListPage1.json").json()

pok_range = range(1, 30)

fetchedPokemons = []
for pok in pok_range:
    requestJson = requests.get(
        "https://raw.githubusercontent.com/arix2000/Pokedex_Data/develop/data/pokemon/pokemonDetails" + str(
            pok) + ".json").json()
    fetchedPokemons.append(requestJson)

print(fetchedPokemons)
print(len(fetchedPokemons))
