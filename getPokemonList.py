import asyncio
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import aiohttp
import requests


def show_types_count_diagram(type_list):
    type_frame = pd.DataFrame(type_list)
    types_names = type_frame.drop_duplicates().to_numpy().flatten()
    count = type_frame.value_counts().values
    plt.style.use('dark_background')
    plt.figure(figsize=(14, 6))
    plt.title("Pokemon Types Counts")
    plt.ylabel("Count")
    plt.bar(types_names, count, width=0.9)
    plt.show()


def get_mapped_types(pok_types):
    mapped_types = []
    for pok_type in pok_types:
        mapped = {"slot": pok_type["slot"], "name": pok_type["type"]["name"]}
        mapped_types.append(mapped)
    return mapped_types


def get_pokemon_details_reduced(pokemon_details):
    wanted_keys = ["id", "name", "types"]
    image_url = pokemon_details["sprites"]["other"]["official-artwork"]["front_default"]
    pokemon_details_filtered = {key: pokemon_details[key] for key in wanted_keys}
    pokemon_details_filtered.update({"image_url": image_url})
    pokemon_details_filtered["types"] = get_mapped_types(pokemon_details["types"])

    return pokemon_details_filtered


async def fetch_pokemon_details(s, pokemon):
    async with s.get(pokemon["url"]) as resp:
        pokemon_details: dict = await resp.json()
        return get_pokemon_details_reduced(pokemon_details)


async def get_pokemon_details_list_from(s, pokemon_basic_request: dict):
    processed_pokemons = 0
    tasks = []
    for pokemon in pokemon_basic_request["results"]:
        task = asyncio.create_task(fetch_pokemon_details(s, pokemon))
        tasks.append(task)
        processed_pokemons += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ProcessedPokemons: " + str(processed_pokemons) + "/" + str(pokemon_basic_request["count"]))

    all_pokemon_details = await asyncio.gather(*tasks)
    with open("./data/pokemon/pokemonDetails.json", 'w') as fp:
        json.dump(all_pokemon_details, fp)

    type_list = []
    for detail in all_pokemon_details:
        type_list.append(detail["types"][0]["name"])

    show_types_count_diagram(type_list)


async def main():
    current_pokemon_basic_data: dict = requests.get(
        "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0").json()

    session = aiohttp.ClientSession()
    await get_pokemon_details_list_from(s=session,
                                        pokemon_basic_request=current_pokemon_basic_data)

    await session.close()


asyncio.run(main())

print("Done")
