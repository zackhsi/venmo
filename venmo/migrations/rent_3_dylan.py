from tinydb import Query

import venmo

Rent = Query()

venmo.rent.update(
    {
        'note': 'Window room',
        'phone': '14153509693',  # Dylan
        'amount': -1716.28,
    },
    Rent.note == 'Window room prorated 2 of 31'
)
