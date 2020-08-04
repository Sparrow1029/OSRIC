import requests
import json

base_url = "http://localhost:5000/api"

login_url = base_url + "/auth/login"
headers = {"Content-Type": "application/json"}


def get_jwt(username, password):
    creds = json.dumps({"username": username, "password": password})
    login = requests.post(login_url, data=creds, headers=headers)
    token = login.json()["token"]
    return token
