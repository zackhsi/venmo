import atexit

from venmo import cookies, singletons

__version__ = '0.3.1'


def exit_handler():
    cookies.save(singletons.session().cookies)

atexit.register(exit_handler)
