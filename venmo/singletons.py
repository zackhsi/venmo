from requests import Session
from venmo import cookies

_session = None


def session():
    global _session
    if not _session:
        _session = Session()
        _session.cookies = cookies.load()
    return _session
