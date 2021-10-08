from igdb.wrapper import IGDBWrapper
from pprint import pprint as pp
from dotenv import load_dotenv
import json
import os
from os.path import exists
import requests
import shutil


load_dotenv()
CLIENT_ID = os.getenv("CLIENTID")
ACCESS_TOKEN = os.getenv("ACCESSTOKEN")

wrapper = IGDBWrapper(CLIENT_ID, ACCESS_TOKEN)

byte_array = wrapper.api_request(
            'games',
            """fields id, name, slug, cover, url;
            limit 1; offset 0;
            where genres=(4) & category=0 & cover != null & rating > 50;
            sort rating_count desc;"""
          )

# game_json = json.loads(byte_array.decode('utf-8'))
# pp(game_json)


def get_images(id, genre, offset):
    path = "dataset/" + genre + "/"

    games = json.loads(wrapper.api_request(
            "games",
            f"""fields id, name, slug, cover;
            limit 500; offset {offset};
            where genres=({id}) & category=0 & cover != null & rating > 50;
            sort rating_count desc;"""
          ).decode("utf8"))

    for game in games:
        url = "http://images.igdb.com/igdb/image/upload/t_cover_big/"
        url += json.loads(wrapper.api_request(
              "covers",
              f"fields *; where id={game['cover']};"
              ).decode("utf8"))[0]['image_id'] + ".png"

        slug = game['slug']
        name = game['name']

        if not exists(f"{path}{slug}.png"):
            img = requests.get(url, stream=True)

            if img.status_code == 200:
                img.raw.decode_content = True

                with open(f"{path}{slug}.png", "wb") as file:
                    shutil.copyfileobj(img.raw, file)

                print(f"{name} cover saved as {slug}.png in {path}")
            else:
                print(f"{name} cover not found")
        else:
            print(f"{name} cover already saved in {path}")


# Genres to use: 4 Fighting, 8 Platform, 9 Puzzle, 14 Sport, 32 Indie
get_images("4", "fighting", 0)
get_images("4", "fighting", 500)
get_images("8", "platform", 0)
get_images("8", "platform", 500)
get_images("9", "puzzle", 0)
get_images("9", "puzzle", 500)
get_images("14", "sport", 0)
get_images("14", "sport", 500)
get_images("32", "indie", 0)
get_images("32", "indie", 500)
