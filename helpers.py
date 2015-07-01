import json


def pprint(dictionary):
    print json.dumps(
        dictionary,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )


def log_response(response):
    payment = response.json()['data']['payment']
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
