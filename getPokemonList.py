import asyncio
import json
import os

import aiohttp
import requests


def get_pokemon_details_reduced(pokemon_details):
    wanted_keys = ["id", "name", "types"]
    image_url = pokemon_details["sprites"]["other"]["official-artwork"]["front_default"]
    pokemon_details_filtered = {key: pokemon_details[key] for key in wanted_keys}
    pokemon_details_filtered.update({"image_url": image_url})
    return pokemon_details_filtered


async def fetch_pokemon_details(s, pokemon):

    async with s.get(pokemon["url"]) as resp:
        pokemon_details: dict = await resp.json()
        current_pokemon_basic_data = get_pokemon_details_reduced(pokemon_details)
        with open("./data/pokemon/pokemonDetails" + str(current_pokemon_basic_data["id"]) + ".json", 'w') as fp:
            json.dump(current_pokemon_basic_data, fp)


async def get_pokemon_details_list_from(s, pokemon_basic_request: dict):
    processed_pokemons = 0
    for pokemon in pokemon_basic_request["results"]:
        await asyncio.create_task(fetch_pokemon_details(s, pokemon))
        processed_pokemons += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ProcessedPokemons: " + str(processed_pokemons) + "/" +str(pokemon_basic_request["count"]))


async def main():
    current_pokemon_basic_data: dict = requests.get(
        "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0").json()

    session = aiohttp.ClientSession()
    await get_pokemon_details_list_from(s=session,
                                        pokemon_basic_request=current_pokemon_basic_data)

    await session.close()


asyncio.run(main())

print("Done")
