import os


# OAuth
CLIENT_ID = '2667'
CLIENT_SECRET = 'srDrmU3yf452HuFF63HqHEt25pa5DexZ'

# Paths
DOT_VENMO = os.path.join(os.path.expanduser('~'), '.venmo')
CREDENTIALS_FILE = os.path.join(DOT_VENMO, 'credentials')
COOKIES_FILE = os.path.join(DOT_VENMO, 'cookies')

# URLs
ACCESS_TOKEN_URL = 'https://api.venmo.com/v1/oauth/access_token'
AUTHORIZATION_URL = 'https://api.venmo.com/v1/oauth/authorize'
PAYMENTS_URL = 'https://api.venmo.com/v1/payments'
TWO_FACTOR_URL = 'https://venmo.com/api/v5/two_factor/token'
TWO_FACTOR_AUTHORIZATION_URL = 'https://venmo.com/authorize'
USERS_URL = 'https://api.venmo.com/v1/users'
