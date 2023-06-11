import asyncio
import json
import os

import aiohttp
import requests


def get_ability_details_reduced(ability_details):
    wanted_keys = ["id", "name"]
    ability_details_filtered = {key: ability_details[key] for key in wanted_keys}

    return ability_details_filtered


async def fetch_ability_details(s, ability):
    async with s.get(ability["url"]) as resp:
        ability_details: dict = await resp.json()
        return get_ability_details_reduced(ability_details)


async def get_ability_details_list_from(s, ability_basic_request: dict):
    processed_abilities = 0
    tasks = []
    for ability in ability_basic_request["results"]:
        task = asyncio.create_task(fetch_ability_details(s, ability))
        tasks.append(task)
        processed_abilities += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Processed abilities: " + str(processed_abilities) + "/" + str(ability_basic_request["count"]))

    all_ability_details = await asyncio.gather(*tasks)
    with open("./data/abilityList.json", 'w') as fp:
        json.dump(all_ability_details, fp)


async def main():
    current_ability_basic_data: dict = requests.get(
        "https://pokeapi.co/api/v2/ability?limit=100000&offset=0").json()

    session = aiohttp.ClientSession()
    await get_ability_details_list_from(s=session,
                                        ability_basic_request=current_ability_basic_data)

    await session.close()


asyncio.run(main())

print("Done")
