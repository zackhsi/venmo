import urllib
import webbrowser
import requests

CLIENT_ID = '2667'
CLIENT_SECRET = 'srDrmU3yf452HuFF63HqHEt25pa5DexZ'
BASE_URL = "https://api.venmo.com/v1"


def authorization_url():
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
        'client_id': CLIENT_ID,
        'scope': " ".join(scopes),
        'response_type': 'code',
    }
    return "{base_url}/oauth/authorize?{params}".format(
        base_url=BASE_URL,
        params=urllib.urlencode(params)
    )


def get_code():
    webbrowser.open(authorization_url())
    return raw_input("Code: ")


def get_access_token(authorization_code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": authorization_code,
    }
    url = "https://api.venmo.com/v1/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()
    return response_dict['access_token']


if __name__ == '__main__':
    authorization_code = get_code()
    access_token = get_access_token(authorization_code)
    print access_token
