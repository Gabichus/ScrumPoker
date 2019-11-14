import os

backendAddress = '192.168.100.201'

postgres = {
    'user': 'gabichus',
    'pw': '123',
    'db': 'poker',
    'host': 'localhost'
}

class Config(object):
    SECRET_KEY = 'y5225ou-winvhnhnhll-nc ngcnnmnbhever-v cvncguess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s/%(db)s' % postgres
    SQLALCHEMY_TRACK_MODIFICATIONS = False