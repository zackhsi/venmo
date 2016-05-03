'''
Payment
'''

import logging
import urllib

import venmo

logger = logging.getLogger('venmo.payment')


def pay(user, amount, note):
    _pay_or_charge(user, amount, note)


def charge(user, amount, note):
    amount = -amount
    _pay_or_charge(user, amount, note)


def _pay_or_charge(user, amount, note):
    access_token = venmo.auth.get_access_token()
    if not access_token:
        logger.warn('No access token. Configuring ...')
        if not venmo.auth.configure():
            return
        access_token = venmo.auth.get_access_token()

    params = {
        'note': note,
        'amount': amount,
        'access_token': access_token,
        'audience': 'private',
    }
    if user.startswith('@'):
        username = user[1:]
        user_id = venmo.user.id_from_username(username.lower())
        if not user_id:
            logger.error('Could not find user @{}'.format(username))
            return
        params['user_id'] = user_id.lower()
    else:
        params['phone'] = user
    response = venmo.singletons.session().post(
        _payments_url_with_params(params)
    ).json()
    _print_response(response)


def _payments_url_with_params(params):
    return '{payments_base_url}?{params}'.format(
        payments_base_url=venmo.settings.PAYMENTS_URL,
        params=urllib.urlencode(params),
    )


def _print_response(response):
    if 'error' in response:
        message = response['error']['message']
        code = response['error']['code']
        logger.error('message="{}" code={}'.format(message, code))
        return

    payment = response['data']['payment']
    target = payment['target']

    payment_action = payment['action']
    if payment_action == 'charge':
        payment_action = 'charged'
    if payment_action == 'pay':
        payment_action = 'paid'

    amount = payment['amount']
    if target['type'] == 'user':
        user = '{first_name} {last_name}'.format(
            first_name=target['user']['first_name'],
            last_name=target['user']['last_name'],
        )
    else:
        user = target[target['type']],
    note = payment['note']

    print ('Successfully {payment_action} {user} ${amount:.2f} for "{note}"'
           .format(**locals()))
