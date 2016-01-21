"""
Authentication
"""

import ConfigParser
import getpass
import os
import os.path
import re
import urllib
import xml.etree.ElementTree as ET

import requests

from venmo import settings

session = requests.Session()


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
    redirect_url = response.headers['location']
    if "two-factor" in redirect_url:
        two_factor(redirect_url, auth_request, csrftoken2)
    # TODO: save cookies


def two_factor(redirect_url, auth_request, csrftoken2):
    # Get two factor page
    response = session.get(redirect_url)

    # Send SMS
    secret = extract_otp_secret(response.text)
    headers = {"Venmo-Otp-Secret": secret}
    data = {
        "via": "sms",
        "csrftoken2": csrftoken2,
    }
    url = "{}?{}".format(settings.TWO_FACTOR_URL, urllib.urlencode(data))
    response = session.post(
        url,
        headers=headers,
    )
    assert response.status_code == 200, "Post to 2FA failed"
    assert response.json()['data']['status'] == 'sent', "SMS did not send"

    # Submit verification code
    verification_code = raw_input("Verification code: ")
    headers['Venmo-Otp'] = verification_code
    data = {
        "auth_request": auth_request,
        "csrftoken2": csrftoken2,
    }
    response = session.post(
        settings.TWO_FACTOR_AUTHORIZATION_URL,
        headers=headers,
        json=data,
        allow_redirects=False,
    )
    assert response.status_code == 200, "ERROR: verification code failed"

    # Retrieve access token
    location = response.json()['location']
    code = location.split("code=")[1]
    access_token = retrieve_access_token(code)

    config = read_config()
    config.set(ConfigParser.DEFAULTSECT, 'access_token', access_token)
    write_config(config)
    print "Saved access token!"


def extract_otp_secret(text):
    pattern = re.compile('data-otp-secret="(\w*)"')
    for line in text.splitlines():
        if 'data-otp-secret' in line:
            match = pattern.search(line)
            return match.group(1)
    raise Exception('msg="Could not extract data-otp-secret" text={}'
                    .format(text))


def retrieve_access_token(code):
    data = {
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "code": code,
    }
    response = session.post(settings.ACCESS_TOKEN_URL, data)
    response_dict = response.json()
    access_token = response_dict['access_token']
    return access_token


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
