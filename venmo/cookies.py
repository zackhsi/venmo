import pickle

from venmo import settings
import requests.cookies


def save(requests_cookiejar):
    with open(settings.COOKIES_FILE, 'wb') as f:
        pickle.dump(requests_cookiejar, f)


def load():
    try:
        with open(settings.COOKIES_FILE, 'rb') as f:
            return pickle.load(f)
    except IOError:
        # No cookies
        return requests.cookies.RequestsCookieJar()
