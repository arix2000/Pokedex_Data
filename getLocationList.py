import asyncio
import json
import os

import aiohttp
import requests


def get_location_details_reduced(location_details):
    wanted_keys = ["id", "name", "region"]
    location_details_filtered = {key: location_details[key] for key in wanted_keys}

    return location_details_filtered


async def fetch_location_details(s, location):
    async with s.get(location["url"]) as resp:
        location_details: dict = await resp.json()
        return get_location_details_reduced(location_details)


async def get_location_details_list_from(s, location_basic_request: dict):
    processed_locations = 0
    tasks = []
    for location in location_basic_request["results"]:
        task = asyncio.create_task(fetch_location_details(s, location))
        tasks.append(task)
        processed_locations += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Processed locations: " + str(processed_locations) + "/" + str(location_basic_request["count"]))

    all_location_details = await asyncio.gather(*tasks)
    with open("./data/locationList.json", 'w') as fp:
        json.dump(all_location_details, fp)


async def main():
    current_location_basic_data: dict = requests.get(
        "https://pokeapi.co/api/v2/location?limit=100000&offset=0").json()

    session = aiohttp.ClientSession()
    await get_location_details_list_from(s=session,
                                         location_basic_request=current_location_basic_data)

    await session.close()


asyncio.run(main())

print("Done")
