import requests
import json
import copy

base_url = "http://localhost:5000/api"

login_url = base_url + "/auth/login"
char_url = base_url + "/characters/create"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML,"
    " like Gecko) Chrome/55.0.2883.75 Safari/537.36"
}

test_char1 = {
    "name": "Haladir Olofaren",
    "base_stats": {
        "str": 10,
        "con": 10,
        "dex": 10,
        "int": 10,
        "wis": 10,
        "cha": 10
    },
    "class": "thief",
    "race": "half_elf",
    "gender": "male"
}

test_char2 = {
    "name": "Kordrida Brightdelver",
    "base_stats": {
        "str": 10,
        "con": 10,
        "dex": 10,
        "int": 10,
        "wis": 10,
        "cha": 10
    },
    "class": "druid",
    "race": "halfling",
    "gender": "female"
}


def create_characters():
    creds1 = json.dumps({"username": "sparrow", "password": "password"})
    creds2 = json.dumps({"username": "pellowprincess", "password": "password"})
    login1 = requests.post(login_url, data=creds1, headers=headers)
    login2 = requests.post(login_url, data=creds2, headers=headers)
    print(f"sparrow login: {login1.status_code}")
    print(f"pellowprincess login: {login2.status_code}")
    token1 = login1.json()["token"]
    token2 = login2.json()["token"]
    print(f"sparrow token: {token1}")
    print(f"pellowprincess token: {token2}")

    headers1 = copy.deepcopy(headers)
    headers2 = copy.deepcopy(headers)
    headers1["Authorization"] = f"Bearer {token1}"
    headers2["Authorization"] = f"Bearer {token2}"

    char_ids = {
        "sparrow": {
            "name": "Haladir Olofaren",
            "id": None
        },
        "pellowprincess": {
            "name": "Kordrida Brightdelver",
            "id": None
        }
    }
    print("\nCREATING HALADIR")
    payload = json.dumps(test_char1)
    r = requests.post(char_url, data=payload, headers=headers1)
    print(r.status_code)
    print(r.json())
    char_ids["sparrow"]["id"] = r.json()["id"]

    print("\nCREATING KORDRIDA")
    payload2 = json.dumps(test_char2)
    r2 = requests.post(char_url, data=payload2, headers=headers2)
    print(r2.status_code)
    print(r2.json())
    char_ids["pellowprincess"]["id"] = r2.json()["id"]
    return char_ids
