import atexit

from requests import Session

import venmo

_session = None


def _save_cookies():
    venmo.cookies.save(session().cookies)


def session():
    global _session
    if not _session:
        _session = Session()
        _session.cookies = venmo.cookies.load()
        atexit.register(_save_cookies)
    return _session
