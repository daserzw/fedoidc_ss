import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# DEBUG
DEBUG = True
TRAP_BAD_REQUEST_ERRORS = True

## DB
SQLITE_DB_PATH='sqlite:///' + os.path.join(_basedir, 'data/app.data')

## Signing Service
SIG_KEY = os.path.join(_basedir, 'data/fo_org.jwks')
FO_NAME = 'https://fo.org'
LIFETIME = 300
PORT = 5000

## KEYDEFS
KEYDEFS = [
    {"type": "RSA", "key": '', "use": ["sig"]},
    {"type": "EC", "crv": "P-256", "use": ["sig"]}
]
