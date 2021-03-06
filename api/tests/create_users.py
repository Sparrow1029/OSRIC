import requests
import json

api_url = "http://localhost:5000/api/auth/signup"
headers = {"Content-Type": "application/json"}


def create_users():
    test_user = {
        "username": "sparrow",
        "password": "password",
        "email": "email@example.com",
        "real_name": "Alex Ray"
    }

    payload = json.dumps(test_user)

    r = requests.post(api_url, data=payload, headers=headers)
    if r.status_code not in range(200, 300):
        print(r.status_code, r.text)
        return False

    test_user2 = {
        "username": "pellowprincess",
        "password": "password",
        "email": "email2@example.com",
        "real_name": "Nikki Ray"
    }

    payload = json.dumps(test_user2)

    r = requests.post(api_url, data=payload, headers=headers)
    if r.status_code not in range(200, 300):
        print(r.status_code, r.text)
        return False
    return True
