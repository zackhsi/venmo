from tinydb import TinyDB


db = TinyDB('db.json')
auth = db.table('auth')
rent = db.table('rent')
users = db.table('users')
