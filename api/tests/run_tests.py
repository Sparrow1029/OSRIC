import requests
import time
from pprint import pprint

from login import get_jwt
from create_users import create_users
from create_char import create_characters
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dnd_database
if not len(list(db.player.find())) == 2:
    create_users()

delete_url = "http://localhost:5000/api/characters/delete?character_id={}"


def delete_character(char_id, player_token):
    headers = {
        "Authorization": f"Bearer {player_token}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/55.0.2883.75 Safari/537.36"
    }
    return requests.delete(delete_url.format(char_id), headers=headers, verify=False)


def test_delete_positive():
    # Positive
    characters = create_characters()
    for char in list(db.characters.find()):
        print(char["owner"])
        print(char["available_spells"])
    for player in list(db.player.find()):
        print(player["username"] + " Character list:")
        print(player["characters"])
    # pprint(characters)
    sparrow_token = get_jwt("sparrow", "password")
    pellowprincess_token = get_jwt("pellowprincess", "password")

    print(f"Attempting to delete {characters['sparrow']['name']}...")
    del_req = delete_character(characters["sparrow"]["id"], sparrow_token)
    print(del_req.status_code, del_req.text)

    print(f"Attempting to delete {characters['pellowprincess']['name']}...")
    del_req = delete_character(characters["pellowprincess"]["id"], pellowprincess_token)
    print(del_req.status_code, del_req.text)


if __name__ == "__main__":
    try:
        test_delete_positive()
    except Exception as e:
        print("FUCK", e)
    finally:
        pprint(list(db.player.find()))
        db.player.drop()
        db.characters.drop()
