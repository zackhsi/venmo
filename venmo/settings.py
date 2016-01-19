import os


# OAuth
CLIENT_ID = '2667'
CLIENT_SECRET = 'srDrmU3yf452HuFF63HqHEt25pa5DexZ'

# Files
ACCESS_TOKEN_FILE = "/usr/local/var/venmo/ACCESS_TOKEN"
CREDENTIALS_FILE = os.path.join(os.path.expanduser("~"),
                                ".venmo", "credentials")

# URLs
ACCESS_TOKEN_URL = "https://api.venmo.com/v1/oauth/access_token"
AUTHORIZATION_URL = "https://api.venmo.com/v1/oauth/authorize"
PAYMENTS_URL = "https://api.venmo.com/v1/payments"
USERS_URL = "https://api.venmo.com/v1/users"
