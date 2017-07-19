'''
User module.
'''
import json

import requests

import venmo


def id_from_username(username):
    for u in search(username):
        if u['username'] == username:
            return u['id']
    return None


def print_search(query):
    print(json.dumps(search(query), indent=4))


def search(query):
    response = requests.get(
        venmo.settings.USERS_URL,
        params={
            'limit': 5,
            'query': query,
        }
    )
    users = response.json()['data']
    results = []
    for u in users:
        results.append({
            'id': u['id'],
            'username': u['username'],
            'display_name': u['display_name'],
            'profile_picture_url': u['profile_picture_url'],
        })
    return results
