import logging

from venmo._version import __version__  # noqa

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

logging.getLogger('requests').setLevel(logging.WARNING)
