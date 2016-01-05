from tinydb import Query

import venmo

Rent = Query()

venmo.rent.update(
    {
        'note': 'Window room prorated 2 of 31',
        'amount': -62.99,
    },
    Rent.note == 'Window room'
)
