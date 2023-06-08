import asyncio
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import aiohttp
import requests


def get_pokemon_details_reduced(move_details):
    wanted_keys = ["id", "name", "type"]
    move_details_filtered = {key: move_details[key] for key in wanted_keys}

    return move_details_filtered


async def fetch_move_details(s, move):
    async with s.get(move["url"]) as resp:
        move_details: dict = await resp.json()
        return get_pokemon_details_reduced(move_details)


async def get_moves_details_list_from(s, moves_basic_request: dict):
    processed_moves = 0
    tasks = []
    for move in moves_basic_request["results"]:
        task = asyncio.create_task(fetch_move_details(s, move))
        tasks.append(task)
        processed_moves += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Processed moves: " + str(processed_moves) + "/" + str(moves_basic_request["count"]))

    all_move_details = await asyncio.gather(*tasks)
    with open("./data/moveList.json", 'w') as fp:
        json.dump(all_move_details, fp)


async def main():
    current_moves_basic_data: dict = requests.get(
        "https://pokeapi.co/api/v2/move?limit=100000&offset=0").json()

    session = aiohttp.ClientSession()
    await get_moves_details_list_from(s=session,
                                      moves_basic_request=current_moves_basic_data)

    await session.close()


asyncio.run(main())

print("Done")
