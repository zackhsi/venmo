import json


def pprint(dictionary):
    print json.dumps(
        dictionary,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )


def log_response(response):
    if 'error' in response:
        message = response['error']['message']
        code = response['error']['code']
        print 'message="{}" code={}'.format(message, code)
        return

    payment = response['data']['payment']
    target = payment['target']

    payment_action = payment['action']
    amount = payment['amount']
    if target['type'] == 'user':
        user = "{first_name} {last_name}".format(
            first_name=target['user']['first_name'],
            last_name=target['user']['last_name'],
        )
    else:
        user = target[target['type']],
    note = payment['note']

    print "{payment_action} {user} ${amount} for {note}".format(
        payment_action=payment_action,
        user=user,
        amount=amount,
        note=note,
    )
