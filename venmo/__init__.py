import logging

from ._version import __version__  # noqa

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s: %(levelname)s %(message)s')

logging.getLogger('requests').setLevel(logging.WARNING)

from . import (
    auth,
    cli,
    cookies,
    payment,
    settings,
    singletons,
    types,
    user
)
