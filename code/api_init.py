import requests
import json


def init():

    auth_json = json.load(open('auth_data.json'))

    CLIENT_ID = auth_json["CLIENT_ID"]
    SECRET_KEY = auth_json["SECRET_KEY"]

    data = {
        'grant_type': 'password',
        'username': auth_json["username"],
        'password': auth_json['password']
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    res = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth, 
        data=data, 
        headers=headers)

    TOKEN = res.json()['access_token']
    headers['Authorization'] = f'bearer {TOKEN}'

    return headers