"""
OAuth
"""

import os
import getpass
import urllib
import xml.etree.ElementTree as ET

import requests

from venmo import settings


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
    response = requests.get(_authorization_url())
    authorization_page_xml = response.text
    cookie = response.headers['Set-Cookie']
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
        "username": _prompt_username(),
        "password": _prompt_password(),
        "web_redirect_url": web_redirect_url,
        "csrftoken2": csrftoken2,
        "auth_request": auth_request,
        "grant": 1,
    }
    url = "{}?{}".format(settings.AUTHORIZATION_URL, urllib.urlencode(data))
    response = requests.post(
        url,
        headers={
            'Content-type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
        },
    )

    # Stop here for now ...
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


def _prompt_username():
    return raw_input("Venmo email: ")


def _prompt_password():
    return getpass.getpass(prompt="Venmo password: ")
