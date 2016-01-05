from tinydb import TinyDB


db = TinyDB('db.json')
rent = db.table('rent')
users = db.table('users')
