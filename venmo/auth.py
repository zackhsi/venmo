"""
Authentication
"""

import ConfigParser
import getpass
import os
import os.path
import urllib
import xml.etree.ElementTree as ET

import requests

from venmo import settings


def configure(args=None):
    """Save username and password to config file.

    Entering nothing keeps the current credentials.
    """
    # Read old credentials
    config = read_config()
    try:
        old_email = config.get(ConfigParser.DEFAULTSECT, 'email')
    except ConfigParser.NoOptionError:
        old_email = ''
    try:
        old_password = config.get(ConfigParser.DEFAULTSECT, 'password')
    except ConfigParser.NoOptionError:
        old_password = ''

    # Prompt new credentials
    email = raw_input("Venmo email [{}]: "
                      .format(old_email if old_email else None))
    password = getpass.getpass(prompt="Venmo password [{}]: "
                               .format("*"*10 if old_password else None))
    email = email or old_email
    password = password or old_password
    if not any([email, password]):
        return

    # Write new credentials
    if email:
        config.set(ConfigParser.DEFAULTSECT, 'email', email)
    if password:
        config.set(ConfigParser.DEFAULTSECT, 'password', password)
    write_config(config)


def read_config():
    config = ConfigParser.RawConfigParser()
    config.read(settings.CREDENTIALS_FILE)
    return config


def write_config(config):
    try:
        os.makedirs(os.path.dirname(settings.CREDENTIALS_FILE))
    except OSError:
        pass  # It's okay if directory already exists
    with open(settings.CREDENTIALS_FILE, 'w') as configfile:
        config.write(configfile)


def get_access_token():
    try:
        with open(settings.ACCESS_TOKEN_FILE) as f:
            return f.read()
    except IOError:
        print("""
    Venmo requires an access token. Please run:

        venmo refresh-token
""")
        exit(1)


def refresh_token(args):
    # Get and parse authorization webpage xml and form
    session = requests.Session()
    response = session.get(_authorization_url())
    authorization_page_xml = response.text
    filtered_xml = _filter_script_tags(authorization_page_xml)
    root = ET.fromstring(filtered_xml)
    form = root.find('.//form')
    for child in form:
        if child.attrib.get('name') == 'csrftoken2':
            csrftoken2 = child.attrib['value']
        if child.attrib.get('name') == 'auth_request':
            auth_request = child.attrib['value']
        if child.attrib.get('name') == 'web_redirect_url':
            web_redirect_url = child.attrib['value']

    # Submit form
    data = {
        "username": get_username(),
        "password": get_password(),
        "web_redirect_url": web_redirect_url,
        "csrftoken2": csrftoken2,
        "auth_request": auth_request,
        "grant": 1,
    }
    url = "{}?{}".format(settings.AUTHORIZATION_URL, urllib.urlencode(data))
    response = session.post(url, allow_redirects=False)

    assert response.status_code == 302, "ERROR: expecting a redirect"
    print "Redirect to: {}".format(response.headers['location'])
    exit(0)

    authorization_code = raw_input("Code: ")
    data = {
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "code": authorization_code,
    }
    response = requests.post(settings.ACCESS_TOKEN_URL, data)
    response_dict = response.json()
    access_token = response_dict['access_token']
    try:
        os.makedirs(os.path.dirname(settings.ACCESS_TOKEN_FILE))
    except OSError:
        # It's okay if directory already exists
        pass
    with open(settings.ACCESS_TOKEN_FILE, 'w') as f:
        f.write(access_token)


def _authorization_url():
    scopes = [
        'make_payments',
        'access_feed',
        'access_profile',
        'access_email',
        'access_phone',
        'access_balance',
        'access_friends',
    ]
    params = {
        'client_id': settings.CLIENT_ID,
        'scope': " ".join(scopes),
        'response_type': 'code',
    }
    return "{authorization_url}?{params}".format(
        authorization_url=settings.AUTHORIZATION_URL,
        params=urllib.urlencode(params)
    )


def _filter_script_tags(input_xml):
    """Filter out the script so we can parse the xml."""
    output_lines = []
    in_script = False
    for line in input_xml.splitlines():
        if "<script>" in line:
            in_script = True
        if not in_script:
            output_lines.append(line)
        if "</script>" in line:
            in_script = False
    return '\n'.join(output_lines)


def get_username():
    config = read_config()
    try:
        return config.get(ConfigParser.DEFAULTSECT, 'email')
    except ConfigParser.NoOptionError:
        configure()
        return get_username()


def get_password():
    config = read_config()
    try:
        return config.get(ConfigParser.DEFAULTSECT, 'password')
    except ConfigParser.NoOptionError:
        configure()
        return get_password()
