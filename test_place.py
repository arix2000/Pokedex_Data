import asyncio
import requests
import aiohttp
from timeit import default_timer as timer


async def fetch_pokemon(s, pok, from_poke_api):
    if not from_poke_api:
        async with s.get(
                "https://raw.githubusercontent.com/arix2000/Pokedex_Data/develop/data/pokemon/pokemonDetails" + str(
                    pok) + ".json") as resp:
            json_resp = await resp.json(content_type=None)
            return json_resp
    else:
        async with s.get("https://pokeapi.co/api/v2/pokemon/" + str(pok)) as resp:
            json_resp = await resp.json(content_type=None)
            return json_resp


async def get_all(s, from_poke_api):
    pok_range = range(1, 30)
    print("from poke api? :" + str(from_poke_api))
    tasks = []
    for pok in pok_range:
        task = asyncio.create_task(fetch_pokemon(s, pok, from_poke_api))
        tasks.append(task)
    fetched_pokemons = await asyncio.gather(*tasks)
    print(len(fetched_pokemons))


async def main(from_poke_api):
    async with aiohttp.ClientSession() as session:
        await get_all(session, from_poke_api)


start = timer()
asyncio.run(main(False))
end = timer()
print(end - start)
print("-----------------------------------------------------------------------------------------------")
start2 = timer()
asyncio.run(main(True))
end2 = timer()
print(end2 - start2)
