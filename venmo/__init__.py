import atexit

from venmo import cookies, singletons

from venmo._version import __version__  # noqa


def exit_handler():
    cookies.save(singletons.session().cookies)

atexit.register(exit_handler)
