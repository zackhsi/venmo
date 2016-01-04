from tinydb import TinyDB


db = TinyDB('db.json')
users = db.table('users')

users.insert({
    'name': 'Nick Lippis',
    'phone': '16178271991',
})
users.insert({
    'name': 'Zack Morris',
    'phone': '15308591050',
})
users.insert({
    'name': 'Cynthia Laiacona',
    'phone': '15308590976',
})
users.insert({
    'name': 'Kyle Merwin',
    'phone': '14157204626',
})
users.insert({
    'name': 'Rob Garbanati',
    'phone': '19496331541',
})
users.insert({
    'name': 'Nate Siswanto',
    'phone': '18186319598',
})
users.insert({
    'name': 'Ben Hunter',
    'phone': '14153422879',
})
