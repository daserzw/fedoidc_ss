import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# DEBUG
DEBUG = True
TRAP_BAD_REQUEST_ERRORS = True

# DB
SQLITE_DB_PATH='sqlite:///' + os.path.join(_basedir, 'data/app.data')

# ENTITY AND SIGNING
FO_NAME = 'https://fo.org'
FO_SIG_KEYS = os.path.join(_basedir, 'data/fo_org.jwks')
CREATE_FO_JWKS = True
FO_SIG_LIFETIME = 300

# KEYDEFS
KEYDEFS = [
    {"type": "RSA", "key": '', "use": ["sig"]},
    {"type": "EC", "crv": "P-256", "use": ["sig"]}
]
