import logging

from venmo._version import __version__  # noqa

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s: %(levelname)s %(message)s')

logging.getLogger('requests').setLevel(logging.WARNING)

import auth        # noqa
import cli         # noqa
import cookies     # noqa
import payment     # noqa
import settings    # noqa
import singletons  # noqa
import types       # noqa
import user        # noqa
