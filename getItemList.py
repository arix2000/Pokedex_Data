import asyncio
import json
import os

import aiohttp
import requests


def get_item_details_reduced(item_details):
    wanted_keys = ["id", "name", "category"]
    item_details_filtered = {key: item_details[key] for key in wanted_keys}

    return item_details_filtered


async def fetch_item_details(s, item):
    async with s.get(item["url"]) as resp:
        item_details: dict = await resp.json()
        return get_item_details_reduced(item_details)


async def get_item_details_list_from(s, item_basic_request: dict):
    processed_items = 0
    tasks = []
    for item in item_basic_request["results"]:
        task = asyncio.create_task(fetch_item_details(s, item))
        tasks.append(task)
        processed_items += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Processed items: " + str(processed_items) + "/" + str(item_basic_request["count"]))

    all_item_details = await asyncio.gather(*tasks)
    with open("./data/itemList.json", 'w') as fp:
        json.dump(all_item_details, fp)


async def main():
    current_item_basic_data: dict = requests.get(
        "https://pokeapi.co/api/v2/item?limit=100000&offset=0").json()

    session = aiohttp.ClientSession()
    await get_item_details_list_from(s=session,
                                     item_basic_request=current_item_basic_data)

    await session.close()


asyncio.run(main())

print("Done")
