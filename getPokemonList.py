import asyncio
import json
import aiohttp
import requests


async def fetch_pokemon_details(s, url):
    wanted_keys = ["id", "name", "types"]
    async with s.get(url) as resp:
        pokemon_details: dict = await resp.json()
        image_url = pokemon_details["sprites"]["other"]["official-artwork"]["front_default"]
        pokemon_details_filtered = {key: pokemon_details[key] for key in wanted_keys}
        pokemon_details_filtered.update({"image_url": image_url})
        return pokemon_details_filtered


async def get_pokemon_details_list_from(s, pokemon_basic_request: dict) -> list[dict]:
    tasks = []
    for pokemon in pokemon_basic_request["results"]:
        task = asyncio.create_task(fetch_pokemon_details(s, pokemon["url"]))
        tasks.append(task)
    all_pokemon_details = await asyncio.gather(*tasks)
    return all_pokemon_details


async def main():
    limit: int = 30
    offset: int = 0
    iterations = 1
    while True:
        current_pokemon_basic_data: dict = requests.get(
            "https://pokeapi.co/api/v2/pokemon?limit=" + str(limit) + "&offset=" + str(offset) + "").json()

        print("iterations: " + str(iterations) + " limit: " + str(limit) + " offset: " + str(offset))
        async with aiohttp.ClientSession() as session:
            current_pokemon_basic_data["results"] = await get_pokemon_details_list_from(s=session,
                                                                                        pokemon_basic_request=current_pokemon_basic_data)

            with open("./data/pokemon/pokemonListPage" + str(iterations) + ".json", 'w') as fp:
                json.dump(current_pokemon_basic_data, fp)

        if current_pokemon_basic_data["next"] is None:
            break
        offset += limit
        iterations += 1


asyncio.run(main())

print("Done")
