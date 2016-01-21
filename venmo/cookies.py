import os
import pickle

import requests.cookies

from venmo import settings


def save(requests_cookiejar):
    try:
        os.makedirs(os.path.dirname(settings.COOKIES_FILE))
    except OSError:
        pass  # It's okay if directory already exists
    with open(settings.COOKIES_FILE, 'wb') as f:
        pickle.dump(requests_cookiejar, f)


def load():
    try:
        with open(settings.COOKIES_FILE, 'rb') as f:
            return pickle.load(f)
    except IOError:
        # No cookies
        return requests.cookies.RequestsCookieJar()
