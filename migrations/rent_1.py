from tinydb import TinyDB


db = TinyDB('db.json')
rent = db.table('rent')

# rent.insert({
#     'description': 'Bathroom room',
#     'user': 'Zack Hsi',
#     'amount': 1951.28,
# })
rent.insert({
    'description': 'Double room 1',
    'user': 'Rob Garbanati',
    'amount': 976.29,
})
rent.insert({
    'description': 'Double room 2',
    'user': 'Kyle Merwin',
    'amount': 976.28,
})
rent.insert({
    'description': 'Closet room',
    'user': 'Zack Morris',
    'amount': 876.29,
})
rent.insert({
    'description': 'Window room prorated',
    'user': 'Cynthia Laiacona',
    'amount': 1716.28,
})
rent.insert({
    'description': 'Big room',
    'user': 'Nick Lippis',
    'amount': 1961.28,
})
