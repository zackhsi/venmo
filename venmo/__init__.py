import logging

from .__version__ import __version__  # noqa: F401

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s: %(levelname)s %(message)s')

logging.getLogger('requests').setLevel(logging.WARNING)


from . import (  # noqa: F401
    auth,
    cli,
    cookies,
    payment,
    settings,
    singletons,
    types,
    user
)
