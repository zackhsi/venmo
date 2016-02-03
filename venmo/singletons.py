import atexit

from requests import Session

from venmo import cookies

_session = None


def _save_cookies():
    cookies.save(_session.cookies)


def session():
    global _session
    if not _session:
        _session = Session()
        _session.cookies = cookies.load()
        atexit.register(_save_cookies)
    return _session
