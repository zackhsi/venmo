"""
OAuth

TODO: use oauth2 library, perhaps joestump/python-oauth2
"""

import urllib
import webbrowser

import requests

import venmo
from venmo import settings


def _authorization_url():
    scopes = [
        'make_payments',
        'access_feed',
        'access_profile',
        'access_email',
        'access_phone',
        'access_balance',
        'access_friends',
    ]
    params = {
        'client_id': settings.CLIENT_ID,
        'scope': " ".join(scopes),
        'response_type': 'code',
    }
    return "{base_url}/oauth/authorize?{params}".format(
        base_url=settings.BASE_URL,
        params=urllib.urlencode(params)
    )


def get_access_token():
    return venmo.auth.all()[0]['access_token']


def refresh_token(args):
    webbrowser.open(_authorization_url())
    authorization_code = raw_input("Code: ")
    data = {
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "code": authorization_code,
    }
    url = "{}/oauth/access_token".format(settings.BASE_URL)
    response = requests.post(url, data)
    response_dict = response.json()
    access_token = response_dict['access_token']
    venmo.auth.purge()
    venmo.auth.insert({'access_token': access_token})
